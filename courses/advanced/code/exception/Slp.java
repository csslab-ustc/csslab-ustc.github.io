package exception;

import java.util.List;

// The syntax:
// p -> f*
// f -> x() s*
// s -> print(n)
//   | call f()
//   | try s* catch s*
//   | throw
//   | return
class Slp {
    static class Stm {
        sealed interface T
                permits Call, Print, Return, Throw, Try{
        }

        record Call(String f) implements T {
        }

        record Print(int n) implements T {
        }

        record Throw() implements T {
        }

        record Try(List<Stm.T> s1,
                   List<Stm.T> s2) implements T {
        }

        record Return() implements T {
        }
    }

    record Function(String name,
                    List<Stm.T> stms) {
    }

    record Program(List<Function> funcs) {
    }

    // pretty printer
    private static int indentSize = 0;
    private static void indent(){
        indentSize += 3;
    }

    private static void unindent(){
        indentSize -= 3;
    }

    private static void indentPrint(String s) {
        printSpaces();
        System.out.print(s);
    }

    private static void indentPrintln(String s) {
        printSpaces();
        System.out.println(s);
    }

    private static void printSpaces(){
        int i = indentSize;
        while(i-->0)
            System.out.print(" ");
    }

    private static void ppStm(Stm.T s){
        switch (s){
            case Stm.Call(String f) -> {
                indentPrintln(STR."\{f}()");
            }
            case Stm.Print(int n) -> {
                indentPrintln(STR."print(\{n})");
            }
            case Stm.Throw() -> {
                indentPrintln("throw");
            }
            case Stm.Try(List<Stm.T> s1, List<Stm.T> s2) -> {
                indentPrintln("try{");
                indent();
                s1.forEach(Slp::ppStm);
                unindent();
                indentPrintln("}catch{");
                indent();
                s2.forEach(Slp::ppStm);
                unindent();
                indentPrintln("}");
            }
            case Stm.Return() -> {
                indentPrintln("return");
            }
        }
    }

    private static void ppFunc(Function f){
        indentPrintln(STR."// The SLP code:\n\{f.name()}(){");
        indent();
        f.stms().forEach(Slp::ppStm);
        unindent();
        indentPrintln("}");
    }

    public static void pp(Program p){
        p.funcs().forEach(Slp::ppFunc);
    }
}
