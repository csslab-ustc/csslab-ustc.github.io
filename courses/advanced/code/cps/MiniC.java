package cps;

import java.util.List;

public class MiniC {
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
        // pretty printing
        static void pp(T e) {
            switch (e) {
                case Bop(String bop, String x, String y) -> {
                    print("("+x+") "+bop+" ("+y+")");
                }
                case Call(String f, String x) -> {
                    print(f+"("+x+")");
                }
                case Num(int n) -> print(n);
                case Var(String x) -> print(x);
            }
        }

        sealed interface T
                permits Bop, Call, Num, Var {
        }

        record Bop(String bop, String x, String y) implements T {
        }

        record Call(String f, String x) implements T {
        }

        record Num(int n) implements T {
        }

        record Var(String x) implements T {
        }
    }

    static class Stm {
        sealed interface T
                permits Assign, If, Return {
        }

        record Assign(String x, Exp.T e) implements T {
        }

        record If(String op,
                  String x,
                  String y,
                  List<Stm.T> then_,
                  List<Stm.T> else_) implements T {
        }

        record Return(String x) implements T {
        }

        static void pp(T s) {
            switch (s) {
                case Assign(String x, Exp.T e) -> {
                    printSpaces();
                    print(x+" = ");
                    Exp.pp(e);
                    print(";\n");
                }
                case If(String bop, String x, String y,
                        List<Stm.T> then_,
                        List<Stm.T> else_) -> {
                    printSpaces();
                    print("if("+x+" "+bop+" "+y+"){\n");
                    indent();
                    ppStms(then_);
                    unindent();
                    printSpaces();
                    print("}else{\n");
                    indent();
                    ppStms(else_);
                    unindent();
                    printSpaces();
                    print("}\n");
                }
                case Return(String x) -> {
                    printSpaces();
                    print("return "+x+";\n");
                }
            }
        }

        public static void ppStms(List<Stm.T> stms){
            stms.forEach(Stm::pp);
        }
    }

    static class Function {
        sealed interface T
                permits Singleton {
        }

        record Singleton(String name, String arg, List<Stm.T> stms) implements T {
        }

        static void pp(T f) {
            switch (f) {
                case Singleton(String name, String arg, List<Stm.T> stms) -> {
                    printSpaces();
                    print(name+"("+arg+"){\n");
                    indent();
                    Stm.ppStms(stms);
                    unindent();
                    printSpaces();
                    print("}\n");
                }
            }
        }
    }
}
