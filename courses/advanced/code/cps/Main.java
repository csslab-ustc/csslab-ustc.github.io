// Continuation-pass style
package cps;

import java.util.List;

public class Main {

    private static void doit(MiniC.Function.T f) {
        MiniC.Function.pp(f);
        System.out.println();
        // generate a "entry"
        Cps.Function.T cpsF = new Compiler().doit(f);
        Cps.Function.pp(cpsF);
    }

    public static void main(String[] args) {
        // test case1
//        abs(n){
//            if(n<0) y = 0-n;
//            else y = n;
//            return y;
//        }
        MiniC.Function.T f = new MiniC.Function.Singleton("abs", "n",
                List.of(new MiniC.Stm.If("<", "y", "0",
                               List.of(new MiniC.Stm.Assign("y",
                                       new MiniC.Exp.Bop("-", "0", "n"))),
                        List.of(new MiniC.Stm.Assign("y", new MiniC.Exp.Var("n")))),
                        new MiniC.Stm.Return("y")));
        doit(f);
//
//        sum(n){
//            if(n==0) return 0;
//            else return n + sum(n-1); }
        f = new MiniC.Function.Singleton("sum", "n",
                List.of(new MiniC.Stm.If("==", "n", "0",
                        List.of(new MiniC.Stm.Return("0")),
                                List.of(new MiniC.Stm.Assign("t", new MiniC.Exp.Bop("-", "n", "1")),
                                        new MiniC.Stm.Assign("r", new MiniC.Exp.Call("sum", "t")),
                                        new MiniC.Stm.Assign("s", new MiniC.Exp.Bop("+", "n", "r")),
                        new MiniC.Stm.Return("s")))));
        doit(f);

//        fib(n){
//            if(n <= 1)
//                return 1;
//            else{
//                f1 = fib(n - 2);
//                f2 = fib(n - 1);
//                z = f1 + f2;
//                return z;
        f = new MiniC.Function.Singleton("fib", "n",
                List.of(new MiniC.Stm.If("<=", "n", "1",
                        List.of(new MiniC.Stm.Return("1")),
                        List.of(new MiniC.Stm.Assign("t1", new MiniC.Exp.Bop("-", "n", "2")),
                                new MiniC.Stm.Assign("f1", new MiniC.Exp.Call("fib", "t1")),
                                new MiniC.Stm.Assign("t2", new MiniC.Exp.Bop("-", "n", "1")),
                                new MiniC.Stm.Assign("f2", new MiniC.Exp.Call("fib", "t2")),
                                new MiniC.Stm.Assign("z", new MiniC.Exp.Bop("+", "f1", "f2")),
                                new MiniC.Stm.Return("z")))));
        doit(f);
    }
}






