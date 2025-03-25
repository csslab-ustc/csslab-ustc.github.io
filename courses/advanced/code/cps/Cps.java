package cps;

import java.util.List;

public class Cps {
    private static int indentSize = 0;

    private static void indent() {
        indentSize += 3;
    }

    private static void unindent() {
        indentSize -= 3;
    }

    private static void printSpaces() {
        int i = indentSize;
        while (i-- > 0) {
            System.out.print(" ");
        }
    }

    private static void print(Object s) {
        System.out.print(s.toString());
    }

    static class Exp {
        sealed interface T
                permits Bop, Call, Call2, Num, Var {
        }

        record Bop(String bop, String x, String y) implements T {
        }

        record Call(String f, String x) implements T {
        }

        record Call2(String f, String x, String k) implements T {
        }

        record Num(int n) implements T {
        }

        record Var(String x) implements T {
        }

        // pretty printing, to Python-like code
        static void pp(T e) {
            switch (e) {
                case Bop(String bop, String x, String y) -> {
                    print(STR."(\{x}) \{bop} (\{y})");
                }
                case Call(String f, String x) -> {
                    print(STR."\{f}(\{x})");
                }
                case Call2(String f, String x, String k) -> {
                    print(STR."\{f}(\{x}, \{k})");
                }
                case Num(int n) -> print(n);
                case Var(String x) -> print(x);
            }
        }

    }

    static class Stm {
        sealed interface T
                permits Assign, If, NestFun, Return {
        }

        record Assign(String x, Exp.T e) implements T {
        }

        record If(String op,
                  String x,
                  String y,
                  List<T> then_,
                  List<T> else_) implements T {
        }

        record NestFun(String name,
                  String arg,
                  List<T> stms) implements T {
        }

        record Return(String x) implements T {
        }

        static void pp(T s) {
            switch (s) {
                case Assign(String x, Exp.T e) -> {
                    printSpaces();
                    print(STR."\{x} = ");
                    Exp.pp(e);
                    print("\n");
                }
                case If(String bop, String x, String y, List<T> then_, List<T> else_) -> {
                    printSpaces();
                    print(STR."if \{x} \{bop} \{y}:\n");
                    indent();
                    then_.forEach(Stm::pp);
                    unindent();
                    printSpaces();
                    print(STR."else:\n");
                    indent();
                    else_.forEach(Stm::pp);
                    unindent();
                }
                case NestFun(String name,
                             String arg,
                             List<T> stms) ->{
                    printSpaces();
                    print(STR."def \{name}(\{arg}):\n");
                    indent();
                    stms.forEach(Stm::pp);
                    unindent();
                }
                case Return(String x) -> {
                    printSpaces();
                    print(STR."return \{x}\n");
                }
            }
        }
    }

    static class Function {
        sealed interface T
                permits Singleton {
        }

        record Singleton(String name,
                         String arg,
                         String k,
                         List<Stm.T> stms) implements T {
        }

        static void pp(T f) {
            switch (f) {
                case Singleton(String name,
                               String arg,
                               String k,
                               List<Stm.T> stms) -> {
                    printSpaces();
                    print(STR."def \{name}(\{arg}, \{k}):\n");
                    indent();
                    stms.forEach(Stm::pp);
                    unindent();
                    printSpaces();
                    print("\n");
                }
            }
        }
    }
}
