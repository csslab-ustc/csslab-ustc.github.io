// Continuation-pass style
package cps;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Stack;

class FList{
    sealed interface T permits
            Nil, Cons{
    }

    record Cons(Cps.Stm.T head, T tail) implements T{}
    record Nil() implements T{}

    private static void toList0(T flist, LinkedList<Cps.Stm.T> list){
        switch (flist){
            case Cons(Cps.Stm.T head, T tail) ->{
                list.addLast(head);
                toList0(tail, list);
            }
            case Nil() -> {
            }
        }
    }

    public static List<Cps.Stm.T> toList(T flist){
        LinkedList<Cps.Stm.T> list0 = new LinkedList<>();
        toList0(flist, list0);
        return list0;
    }
}


// compiler
public class Compiler {
    private static int varCounter = 0;
    private static String freshVar(String prefix) {
        return STR."\{prefix}_\{varCounter++}";
    }


    private Cps.Exp.T doitExp(MiniC.Exp.T exp){
        switch (exp) {
            case MiniC.Exp.Bop(String bop, String x, String y) -> {
                return new Cps.Exp.Bop(bop, x, y);
            }
            case MiniC.Exp.Call(String f, String x) -> {
                return new Cps.Exp.Call(f, x);
            }
            case MiniC.Exp.Num(int n) -> {
                return new Cps.Exp.Num(n);
            }
            case MiniC.Exp.Var(String x) -> {
                return new Cps.Exp.Var(x);
            }
        }
    }

    private FList.T doitStm(MiniC.Stm.T stm, List<MiniC.Stm.T> curStms, String k, String j){
        switch (stm) {
            case MiniC.Stm.Assign(
                    String xx,
                    MiniC.Exp.Call(String ff, String ax)
            ) -> {
                String a = freshVar("x");
                var r = doitStms(curStms, k, j);
                r = new FList.Cons(new Cps.Stm.Assign(xx, new Cps.Exp.Var(a)), r);
                var fresh = freshVar("cont");
                Cps.Stm.T h = new Cps.Stm.NestFun(fresh,
                        a,
                        FList.toList(r));
                // the call
                String b = freshVar("_");
                var s2 = new Cps.Stm.Assign(b, new Cps.Exp.Call2(ff, ax, fresh));
                return new FList.Cons(h,
                        new FList.Cons(s2, new FList.Nil()));
            }
            case MiniC.Stm.Assign(String x, MiniC.Exp.T e) -> {
                var r = doitStms(curStms, k, j);
                return new FList.Cons(new Cps.Stm.Assign(x, doitExp(e)), r);
            }
            case MiniC.Stm.If(String bop,
                              String x,
                              String y,
                              List<MiniC.Stm.T> then_,
                              List<MiniC.Stm.T> else_) -> {
                String a = freshVar("x");
                var r = doitStms(curStms, k, j);
                var fresh = freshVar("cont");
                Cps.Stm.T h = new Cps.Stm.NestFun(fresh,
                        a,
                        FList.toList(r));
                var r1 = doitStms(then_, k, fresh);
                var r2 = doitStms(else_, k, fresh);
                var s2 = new Cps.Stm.If(bop, x, y, FList.toList(r1), FList.toList(r2));
                return new FList.Cons(h, new FList.Cons(s2, new FList.Nil()));
            }
            case MiniC.Stm.Return(String x) -> {
                String wild = freshVar("_");
                return new FList.Cons(new Cps.Stm.Assign(wild, new Cps.Exp.Call(k, x)), new FList.Nil());
            }
        }
    }

    private FList.T doitStms(List<MiniC.Stm.T> stms, String k, String j){
//        enterScope();
        if(stms.isEmpty()) {
            return new FList.Cons(new Cps.Stm.Assign("___", new Cps.Exp.Call(j, "0")),
                    new FList.Nil());
        }
        return doitStm(stms.getFirst(), stms.subList(1, stms.size()), k, j);
//        return exitScope();
    }

    public Cps.Function.T doit(MiniC.Function.T f) {
        switch (f){
            case MiniC.Function.Singleton(String name,
                                          String arg,
                                          List<MiniC.Stm.T> stms) -> {
                String k = freshVar("k");
                String j = k;
                var r = doitStms(stms, k, j);
                return new Cps.Function.Singleton(name,
                        arg,
                        k,
                        FList.toList(r));
            }
        }

    }

}