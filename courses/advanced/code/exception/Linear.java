package exception;

import java.util.List;

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
                System.out.println("\tcall "+f+"()");
            }
            case Stm.Jmp(String label) -> System.out.println("\tjmp "+label);
            case Stm.Label(String label) -> {
                System.out.println(label+":");
            }
            case Stm.PopExnFrame() -> System.out.println("\tpop_exn_frame");
            case Stm.PushExnFrame(String f) -> System.out.println("\tpush_exn_frame("+f+")");
            case Stm.Print(int n) -> {
                System.out.println("\tprint("+n+")");
            }
            case Stm.Resume() -> System.out.println("\tresume");
            case Stm.Return() -> System.out.println("\treturn");
            case Stm.Throw() -> System.out.println("\tthrow");
        }
    }

    private static void ppFunc(Function f) {
        System.out.println("fun "+f.name+"()}():");
        f.stms().forEach(Linear::ppStm);
    }

    public static void pp(Program program) {
        program.funcs().forEach(Linear::ppFunc);
    }
}
