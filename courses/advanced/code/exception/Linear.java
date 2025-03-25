package exception;

import java.util.List;
import java.util.Stack;

// linear code:
// p -> f*
// f -> x() s*
// s ->
class Linear {
    class Stm {
        sealed interface T
                permits Call,
                Jmp,
                Label,
                Print,
                PopExnFrame,
                PushExnFrame,
                Resume,
                Return,
                Throw {
        }

        record Call(String f) implements T {
        }

        record Jmp(String name) implements T {
        }

        record Label(String name) implements T {
        }

        record Print(int n) implements T {
        }

        record PopExnFrame() implements T {
        }

        record PushExnFrame(String f) implements T {
        }

        record Resume() implements T {
        }

        record Return() implements T {
        }

        record Throw() implements T {
        }
    }

    record Function(String name, List<Stm.T> stms) {
    }

    record Program(List<Function> funcs) {
    }

    private static void ppStm(Stm.T stm) {
        switch (stm) {
            case Stm.Call(String f) -> {
                System.out.println(STR."\tcall \{f}()");
            }
            case Stm.Jmp(String label) -> System.out.println(STR."\tjmp \{label}");
            case Stm.Label(String label) -> {
                System.out.println(STR."\{label}:");
            }
            case Stm.PopExnFrame() -> System.out.println(STR."\tpop_exn_frame");
            case Stm.PushExnFrame(String f) -> System.out.println(STR."\tpush_exn_frame(\{f})");
            case Stm.Print(int n) -> {
                System.out.println(STR."\tprint(\{n})");
            }
            case Stm.Resume() -> System.out.println(STR."\tresume");
            case Stm.Return() -> System.out.println(STR."\treturn");
            case Stm.Throw() -> System.out.println(STR."\tthrow");
        }
    }

    private static void ppFunc(Function f) {
        System.out.println(STR."fun \{f.name()}():");
        f.stms().forEach(Linear::ppStm);
    }

    public static void pp(Program program) {
        program.funcs().forEach(Linear::ppFunc);
    }
}
