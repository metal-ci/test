import json
import sys


class Control:
    enter  = "enter"
    exit   = "exit"
    cancel = "cancel"


class Level:
    info = "info"
    warning   = "expect"
    assertion = "assert"


class Scope:
    def __init__(self, name):
        self.executed = 0
        self.errors = 0
        self.warnings = 0
        self.children = []
        self.tests = []
        self.cancelled = False
        self.parent = None
        self.name = name
        self.description = None

    def __iadd__(self, rhs):
        self.executed += rhs.executed
        self.errors += rhs.errors
        self.warnings += rhs.warnings
        self.children.append(rhs)
        return self

    #def cancel(self, ):

    def append_test(self, data):
        if "level" in data and "condition" in data:
            self.executed += 1
            if not data["condition"]:
                if data["level"] == "assert":
                    self.errors += 1
                elif data["level"] == "expect":
                    self.warnings += 1

            self.tests.append(data)

    def to_dict(self):
        res = {
            "summary": {
                "executed": self.executed,
                "warnings": self.warnings,
                "errors": self.errors
            },
            "cancelled": self.cancelled,
            "children": [ch.to_dict() for ch in self.children],
            "tests":    self.tests
        }
        if self.description:
            res["description"] = self.description
        return res


class MainScope(Scope):
    def __init__(self):
        super().__init__('<main>')


def loc_str(file, line):
    return "{}({})".format(file.replace('\\\\', '\\'), line)


def message_str(file, line, level, condition):
    return loc_str(file, line) + (" assertion " if level == "assert" else " expectation ") + ("succeeded " if condition else "failed ")


class Reporter:
    def __init__(self):
        self.hrf_sink = sys.stdout
        self.print_level = 'warning' # all, warning error
        self.json_sink = None

        self.__scope_stack = [MainScope()]

    def should_print(self, level = Level.info, condition = 1):
        if self.hrf_sink is None:
            return False

        if self.print_level == 'all':
            return True

        if self.print_level == 'warning':
            return (not condition) and level >= Level.warning

        return (not condition) and level == Level.assertion

    @property
    def current_scope(self):
        return self.__scope_stack[len(self.__scope_stack) - 1]

    def critical(self, file, line, control):
        if self.hrf_sink:
            self.hrf_sink.write("{} critical check failed, cancelling\n".format(loc_str(file, line)))
            self.current_scope.cancelled = True
        self.current_scope.append_test({"type": "critical", "file": file, "line": line, "control": control})

    def loop(self, file, line, control):
        if self.hrf_sink:
            self.hrf_sink.write("{} for loop cancelled\n".format(loc_str(file, line)))
        self.current_scope.append_test({"type": "loop", "file": file, "line": line, "control": control})

    def ranged(self, file, line, control, condition_or_length, range_info, range_info_values=None):
        data = {"type": "ranged", "file": file, "line": line, "control": control, "length": condition_or_length, "control": control}

        if control == "cancel":
            if self.hrf_sink:
                self.hrf_sink.write("{} ranged test cancelled at pos {}\n".format(loc_str(file, line), condition_or_length))
        elif control =="exit":
            if self.hrf_sink:
                self.hrf_sink.write("{} ranged test completed with {} elements\n".format(loc_str(file, line), condition_or_length))
        elif control == 'enter':
            lhs, lhs_len, rhs, rhs_len = range_info
            data['range_info'] = {'lhs': lhs, 'lhs_len': lhs_len, 'rhs': rhs, 'rhs_len': rhs_len}
            if range_info_values:
                lhs_v, lhs_len_v, rhs_v, rhs_len_v = range_info_values
                data['range_info_values'] = {'lhs': lhs_v, 'lhs_len': lhs_len_v, 'rhs': rhs_v, 'rhs_len': rhs_len_v}
                self.hrf_sink.write("{} ranged test starting with {} elements for {}[0 ... {}] and {}[0 ... {}]: [{}[0 ... {}], {}[0 ... {}]]\n"
                                    .format(loc_str(file, line), condition_or_length, lhs, lhs_len, rhs, rhs_len, lhs_v, lhs_len_v, rhs_v, rhs_len_v))
            else:
                self.hrf_sink.write("{} ranged test starting with {} elements for {}[0 ... {}] and {}[0 ... {}]\n"
                                    .format(loc_str(file, line), condition_or_length, lhs, lhs_len, rhs, rhs_len))
        else:
            raise Exception("Unknown control {}".format(control))

        self.current_scope.append_test(data)

    def call(self, file, line, control, condition, function, description=None):
        if control == 'enter':
            scp = Scope(function if function else "**unknown**")
            scp.parent = self.current_scope
            if description:
                scp.description = description
            self.__scope_stack.append(scp)
            self.hrf_sink.write("{} entering test case {}\n"
                                .format(loc_str(file, line), (" " + description) if description else function))
        elif control == 'exit':
            sc = self.current_scope
            self.hrf_sink.write("{} {} test case {}, {} with : {{executed: {}, warnings: {}, errors: {}}}\n"
                                .format(loc_str(file, line),
                                        'cancelling' if sc.cancelled else 'exiting',
                                        (" " + description) if description else function,
                                        ("succeeded " if condition == 0 else "failed "),
                                        sc.executed, sc.warnings, sc.errors))

            self.__scope_stack.pop()
            self.__scope_stack[len(self.__scope_stack) - 1] += sc
        else:
            raise Exception('Unknown control {}'.format(control))

    def log(self, file, line, message):
        if self.hrf_sink:
            self.hrf_sink.write("{} log: {}\n".format(loc_str(file, line), message))
        self.current_scope.append_test({"type": "log", "file": file, "line": line, "message": message})

    def checkpoint(self, file, line):
        if self.should_print():
            self.hrf_sink.write("{} checkpoint\n".format(loc_str(file, line)))
        self.current_scope.append_test({"type": "checkpoint", "file": file, "line": line})

    def message(self, file, line, level, condition, message):
        if self.hrf_sink:
            self.hrf_sink.write("{} message: {}\n".format(message_str(file, line, level, condition), message))
        self.current_scope.append_test({"type": "message", "file": file, "line": line, "message": message, "level": level, "condition": condition})

    def plain  (self, file, line, level, condition, description, value):
        if self.hrf_sink and value:
            self.hrf_sink.write("{} [plain]: {}: [{}]\n".format(message_str(file, line, level, condition), description, value))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [plain]: {}\n".format(message_str(file, line, level, condition), description))
        self.current_scope.append_test({"type": "plain", "file": file, "line": line, "description": description, "level": level, "condition": condition})

    def equal(self, file, line, level, condition, lhs, rhs, lhs_val=None, rhs_val=None):
        ex = '{} == {}'.format(lhs, rhs) if rhs else lhs
        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [equal]: {}: [{} == {}]\n".format(message_str(file, line, level, condition), ex, lhs_val, rhs_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [equal]: {}\n".format(message_str(file, line, level, condition), ex))
        self.current_scope.append_test({"type": "equal", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val})

    def not_equal(self, file, line, level, condition, lhs, rhs, lhs_val=None, rhs_val=None):
        ex = '{} != {}'.format(lhs, rhs) if rhs else lhs
        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [not_equal]: {}: [{} != {}]\n".format(message_str(file, line, level, condition), ex, lhs_val, rhs_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [not_equal]: {}\n".format(message_str(file, line, level, condition), ex))
        self.current_scope.append_test({"type": "not_equal", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val})

    def ge(self, file, line, level, condition, lhs, rhs, lhs_val=None, rhs_val=None):
        ex = '{} >= {}'.format(lhs, rhs) if rhs else lhs
        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [ge]: {}: [{} >= {}]\n".format(message_str(file, line, level, condition), ex, lhs_val, rhs_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [ge]: {}\n".format(message_str(file, line, level, condition), ex))
        self.current_scope.append_test({"type": "ge", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val})

    def le(self, file, line, level, condition, lhs, rhs, lhs_val=None, rhs_val=None):
        ex = '{} <= {}'.format(lhs, rhs) if rhs else lhs
        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [le]: {}: [{} <= {}]\n".format(message_str(file, line, level, condition), ex, lhs_val, rhs_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [le]: {}\n".format(message_str(file, line, level, condition), ex))
        self.current_scope.append_test({"type": "le", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val})

    def greater(self, file, line, level, condition, lhs, rhs, lhs_val=None, rhs_val=None):
        ex = '{} > {}'.format(lhs, rhs) if rhs else lhs
        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [greater]: {}: [{} > {}]\n".format(message_str(file, line, level, condition), ex, lhs_val, rhs_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [greater]: {}\n".format(message_str(file, line, level, condition), ex))
        self.current_scope.append_test({"type": "greater", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val})

    def lesser(self, file, line, level, condition, lhs, rhs, lhs_val=None, rhs_val=None):
        ex = '{} < {}'.format(lhs, rhs) if rhs else lhs
        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [lesser]: {}: [{} < {}]\n".format(message_str(file, line, level, condition), ex, lhs_val, rhs_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [lesser]: {}\n".format(message_str(file, line, level, condition), ex))
        self.current_scope.append_test({"type": "lesser", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val})

    def close(self, file, line, level, condition, lhs, rhs, tolerance, lhs_val=None, rhs_val=None, tolerance_val=None):
        expression = lhs
        if rhs and tolerance:
            expression = '{} = {}  +- ~ {}'.format(lhs, rhs, tolerance)

        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [close]: {}: [{} = {}  +- {}]\n".format(message_str(file, line, level, condition), expression, lhs_val, rhs_val, tolerance_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [close]: {}\n".format(message_str(file, line, level, condition), expression))
        self.current_scope.append_test({"type": "close", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val, "tolerance": tolerance, "tolerance_val": tolerance_val})

    def close_relative(self, file, line, level, condition, lhs, rhs, tolerance, lhs_val=None, rhs_val=None, tolerance_val=None):

        expression = lhs
        if rhs and tolerance:
            expression = '{} = {}  +- ~ {}'.format(lhs, rhs, tolerance)

        if self.hrf_sink and lhs_val and rhs_val:
            self.hrf_sink.write("{} [close_relative]: {}: [{} = {} +- ~ {}]\n".format(message_str(file, line, level, condition), expression, lhs_val, rhs_val, tolerance_val))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [close_relative]: {}\n".format(message_str(file, line, level, condition), expression))
        self.current_scope.append_test({"type": "close", "file": file, "line": line, "lhs" : lhs, "rhs": rhs, "level": level, "condition": condition, "lhs_val" : lhs_val, "rhs_val": rhs_val, "tolerance": tolerance, "tolerance_val": tolerance_val})

    def predicate(self, file, line, level, condition, function, args, function_val=None, args_val=None):
        if self.hrf_sink and function_val and args_val:
            self.hrf_sink.write("{} [predicate]: {}({}): [{}({})]\n".format(message_str(file, line, level, condition), function, ', '.join(args),  function_val, ', '.join(args_val)))
        elif self.hrf_sink:
            self.hrf_sink.write("{} [predicate]: {}({})\n".format(message_str(file, line, level, condition), function, ', '.join(args)))
        self.current_scope.append_test({"type": "close", "file": file, "line": line, "function": function, "args": args, "level": level, "condition": condition, "function_val": function_val, "args_val": args_val})

    def report(self, file, line, condition):
        if self.hrf_sink:
            self.hrf_sink.write("{}: full test report: {{executed: {}, warnings: {}, errors: {}}}\n"
                                .format(loc_str(file, line), self.__scope_stack[0].executed, self.__scope_stack[0].warnings, self.__scope_stack[0].errors))

        if self.json_sink:
            self.json_sink.write(json.dumps(self.__scope_stack[0].to_dict()))
