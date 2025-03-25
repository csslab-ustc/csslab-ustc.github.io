// Closure conversion
package closure;

import java.util.LinkedList;
import java.util.List;

class Lambda {
    sealed interface T
            permits Abs, Add, App, Num, Var {
    }

    record Abs(String x, T e) implements T {
    }

    record Add(T e1, T e2) implements T {
    }

    record App(T e1, T e2) implements T {
    }

    record Num(int n) implements T {
    }

    record Var(String x) implements T {
    }

    // pretty printing
    static void pp(T e) {
        switch (e) {
            case Abs(String x, T e1) -> {
                System.out.print(STR."(\{x})->(");
                pp(e1);
                System.out.print(")");
            }
            case Add(T e1, T e2) -> {
                System.out.print(STR."(");
                pp(e1);
                System.out.print(")+");
                System.out.print(STR."(");
                pp(e2);
                System.out.print(")");
            }
            case App(T e1, T e2) -> {
                System.out.print(STR."(");
                pp(e1);
                System.out.print(").");
                System.out.print(STR."(");
                pp(e2);
                System.out.print(")");
            }
            case Num(int n) -> System.out.print(n);
            case Var(String x) -> System.out.print(x);
        }
    }

    // compiler
    static int varCounter = 0;

    static String freshVar(String prefix) {
        return STR."\{prefix}_\{varCounter++}";
    }

    record Func(String name, String env, String arg, List<String> stms) {
        public Func(String name, String env, String arg) {
            this(name, env, arg, new LinkedList<>());
        }
    }

    // to hold all generated functions:
    static LinkedList<Func> allFuncs = new LinkedList<>();
    // internal libs:
    static List<Func> libs = List.of(
            new Func("build_env", "pair", "env",
                    List.of("return [pair, env]")),
            new Func("build_closure", "f", "env",
                    List.of("return [f, env]")),
            new Func("env_lookup", "env", "x",
                    List.of("pair = env[0]",
                            "tail = env[1]",
                            "if pair[0] == x:",
                            "\treturn pair[1]",
                                "return env_lookup(tail, x)")),
            new Func("call_closure", "c", "x",
                    List.of("code = c[0]",
                            "env = c[1]",
                            "return code(env, x)"))
    );

    // the current function we are generating code for:
    static Func currentFunc = null;

    static Func freshFunc(String arg) {
        Func f = new Func(freshVar("f"), "env", arg);
        allFuncs.add(f);
        return f;
    }

    // print out Python-like code, so that it executes without typing...
    static void printFunc(Func f) {
        System.out.println(STR."def \{f.name}(\{f.env()}, \{f.arg()}):");
        for (String s : f.stms())
            System.out.println(STR."\t\{s}");
    }

    static void printAllFuncsBeforeClear() {
        for (Func f : libs) {
            printFunc(f);
        }
        for (Func f : allFuncs) {
            printFunc(f);
        }
        allFuncs.clear();
    }

    static void emit(String stm) {
        currentFunc.stms.add(stm);
    }

    static String compile(T e, String env) {
        switch (e) {
            case Abs(String x, T e1) -> {
                Func f = freshFunc(x);
                String closure = freshVar("closure");
                emit(STR."\{closure} = build_closure(\{f.name()}, \{env})");
                // begin inner function
                Func oldFunc = currentFunc;
                currentFunc = f;
                String newEnv = freshVar("env");
                emit(STR."\{newEnv} = build_env([\"\{x}\", \{x}], env)");
                String r = compile(e1, newEnv);
                emit(STR."return \{r}");
                // end inner function
                currentFunc = oldFunc;
                return closure;
            }
            case Add(T e1, T e2) -> {
                String x1 = compile(e1, env);
                String x2 = compile(e2, env);
                String x = freshVar("x");
                emit(STR."\{x} = \{x1} + \{x2}");
                return x;
            }
            case App(T e1, T e2) -> {
                String x1 = compile(e1, env);
                String x2 = compile(e2, env);
                String x = freshVar("x");
                emit(STR."\{x} = call_closure(\{x1}, \{x2})");
                return x;
            }
            case Num(int n) -> {
                String x = freshVar("x");
                emit(STR."\{x} = \{n}");
                return x;
            }
            case Var(String y) -> {
                String x = freshVar("x");
                emit(STR."\{x} = env_lookup(\{env}, \"\{y}\")");
                return x;
            }
        }
    }
}

public class Main {

    private static void doit(Lambda.T e) {
        Lambda.pp(e);
        System.out.println();
        // generate a "entry"
        Lambda.Func entry = Lambda.freshFunc("x");
        Lambda.currentFunc = entry;
        String r = Lambda.compile(e, "env");
        Lambda.emit(STR."return \{r}");
        Lambda.printAllFuncsBeforeClear();
        // generate a "main"
        System.out.println(STR."if __name__ == \"__main__\":");
        System.out.println(STR."\tprint(\{entry.name()}(0, 0))");
        System.out.println("\n");
    }

    public static void main(String[] args) {
        // 8
        Lambda.T e = new Lambda.Num(8);
        doit(e);

        // lambda x.x
        e = new Lambda.Abs("x", new Lambda.Var("x"));
        doit(e);

        // (lambda x.x) 88
        e = new Lambda.App(new Lambda.Abs("x", new Lambda.Var("x")),
                new Lambda.Num(88));
        doit(e);

        // (lambda x.lambda y.x) 88 99
        e = new Lambda.App(new Lambda.App(new Lambda.Abs("x",
                new Lambda.Abs("y", new Lambda.Var("x"))),
                new Lambda.Num(88)), new Lambda.Num(99));
        doit(e);

        // (lambda x.x) (lambda y.y) 99
        e = new Lambda.App(new Lambda.Abs("x", new Lambda.Var("x")),
                new Lambda.Abs("x", new Lambda.Var("x")));
        doit(e);
    }
}






