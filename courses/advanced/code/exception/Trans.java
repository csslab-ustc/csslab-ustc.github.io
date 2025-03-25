package exception;

import java.util.LinkedList;
import java.util.List;

// translate Slp to Linear
class Trans{
    // a global list to cache the generated statements
    private LinkedList<Linear.Stm.T> gStms = new LinkedList<>();
    private void emit(Linear.Stm.T s){
        gStms.add(s);
    }

    private static int gLabelCounter = 0;
    private String freshLabel(){
        return STR."L_\{gLabelCounter++}";
    }

    private void doitStm(Slp.Stm.T stm){
        switch (stm) {
            case Slp.Stm.Call(String f) -> {
                emit(new Linear.Stm.Call(f));
            }
            case Slp.Stm.Print(int n) -> emit(new Linear.Stm.Print(n));
            case Slp.Stm.Throw() -> {
                emit(new Linear.Stm.Throw());
            }
            case Slp.Stm.Try(List<Slp.Stm.T> s1, List<Slp.Stm.T> s2) -> {
                String L1 = freshLabel();
                String L2 = freshLabel();
                String L3 = freshLabel();
                emit(new Linear.Stm.Label(L1));
                // s1
                // push handler:
                emit(new Linear.Stm.PushExnFrame(L2));
                s1.forEach(this::doitStm);
                emit(new Linear.Stm.PopExnFrame());
                emit(new Linear.Stm.Jmp(L3));
                emit(new Linear.Stm.Label(L2));
                emit(new Linear.Stm.PopExnFrame());
                // s2
                s2.forEach(this::doitStm);
                emit(new Linear.Stm.Jmp(L3));
                emit(new Linear.Stm.Label(L3));
            }
            case Slp.Stm.Return() -> {
//                emit(new Linear.Stm.PopExnFrame());
                emit(new Linear.Stm.Return());
            }
        }
    }

    private Linear.Function doitFunc(Slp.Function f){
        gStms = new LinkedList<Linear.Stm.T>();
        String L1 = freshLabel();
        String L2 = freshLabel();
//        String L3 = freshLabel();
        emit(new Linear.Stm.Label(L1));
        // stm
        // push the default handler for a function:
        emit(new Linear.Stm.PushExnFrame(L2));
        // generate code for "f"
        f.stms().forEach(this::doitStm);
        emit(new Linear.Stm.Label(L2));
        // a fake handler to resume the function
//        emit(new Linear.Stm.PopExnFrame());
        emit(new Linear.Stm.Resume());
        return new Linear.Function(f.name(), gStms);
    }

    public Linear.Program doit(Slp.Program prog){
        return new Linear.Program(prog.funcs().stream().map(this::doitFunc).toList());
    }
}
