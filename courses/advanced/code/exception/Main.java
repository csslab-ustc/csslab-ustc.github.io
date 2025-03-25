// Exception
package exception;

import java.util.List;

public class Main {

    public static void main(String[] args) {
        // fun main(){
        //   try
        //      print(3);
        //   catch
        //      print(4);
        //   return;
        // }
        Slp.Function entry = new Slp.Function("main",
                List.of(new Slp.Stm.Try(List.of(new Slp.Stm.Print(3)),
                                List.of(new Slp.Stm.Print(4))),
                        new Slp.Stm.Return()));

        Slp.Program prog = new Slp.Program(List.of(entry));
        Slp.pp(prog);
        Linear.Program linear = new Trans().doit(prog);
        Linear.pp(linear);
        new Codegen("a.s").doit(linear);

        // fun main(){
        //   try
        //      throw;
        //   catch
        //      print(4);
        //   return;
        // }
        entry = new Slp.Function("main",
                List.of(new Slp.Stm.Try(List.of(new Slp.Stm.Throw()),
                                List.of(new Slp.Stm.Print(4))),
                        new Slp.Stm.Return()));
        prog = new Slp.Program(List.of(entry));
        Slp.pp(prog);
        linear = new Trans().doit(prog);
        Linear.pp(linear);
        new Codegen("b.s").doit(linear);


        // fun f(){
        //   print(9);
        //   throw;
        //   return;
        // }
        //
        // fun main(){
        //   try
        //      f();
        //   catch
        //      print(4);
        //   return;
        // }
        entry = new Slp.Function("main",
                List.of(new Slp.Stm.Try(List.of(new Slp.Stm.Call("f")),
                                List.of(new Slp.Stm.Print(4))),
                        new Slp.Stm.Return()));
        Slp.Function f = new Slp.Function("f",
                List.of(new Slp.Stm.Print(9),
                        new Slp.Stm.Throw(),
                        new Slp.Stm.Return()));

        prog = new Slp.Program(List.of(f, entry));
        Slp.pp(prog);

        linear = new Trans().doit(prog);
        Linear.pp(linear);
        new Codegen("c.s").doit(linear);

        // fun main(){
        //   throw;
        //   return;
        // }
        entry = new Slp.Function("main",
                List.of(new Slp.Stm.Throw(),
                        new Slp.Stm.Return()));

        prog = new Slp.Program(List.of(entry));
        Slp.pp(prog);
        linear = new Trans().doit(prog);
        Linear.pp(linear);
        new Codegen("d.s").doit(linear);

        var _ = 0;
    }
}






