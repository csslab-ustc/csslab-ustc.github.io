package exception;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

// generate x64 code from "Linear"
class Codegen {
    private String fileName;
    private String gFuncName;
    private OutputStreamWriter writer;

    public Codegen(String fileName) {
        this.fileName = fileName;
    }

    private void emit(String s) {
        try {
            writer.write("\t"+s+"\n");
        } catch (IOException e) {
            throw new AssertionError(e);
        }
    }

    private void emitWithTab(String s) {
        emit("\t"+s);
    }

    private void doitStm(Linear.Stm.T stm) {
        switch (stm) {
            case Linear.Stm.Call(String f) -> {
                emitWithTab("callq\t"+f);
            }
            case Linear.Stm.Jmp(String l) -> {
                emitWithTab("jmp\t"+l);
            }
            case Linear.Stm.Label(String l) -> {
                emit(l+":");
            }
            case Linear.Stm.Print(int n) -> {
                emitWithTab("movq\t$"+n+", %rdi");
                emitWithTab("callq\tprint");
            }
            case Linear.Stm.PopExnFrame() -> {
                emitWithTab("callq\texn_frame_pop");
            }
            case Linear.Stm.PushExnFrame(String l) -> {
                emitWithTab("leaq\t"+l+"(%rip), %rdi");
                emitWithTab("callq\texn_frame_push");
            }
            case Linear.Stm.Resume() -> {
                emitWithTab("callq\texn_frame_pop");
                emitWithTab("leaq\t"+gFuncName+"_name(%rip), %rdi");
                emitWithTab("callq\tcleanup");
                emitWithTab("callq\texn_frame_pop");
                emitWithTab("movq\t%rax, 8(%rbp)");
                emitWithTab("// restore context");
                emitWithTab("leave");
                emitWithTab("ret");
            }
            case Linear.Stm.Return() -> {
                emitWithTab("callq\texn_frame_pop");
                emitWithTab("// restore context");
                emitWithTab("leave");
                emitWithTab("ret");
            }
            case Linear.Stm.Throw() -> {
                emitWithTab("call throw0");
                emitWithTab("jmp\t*%rax");
            }
        }
    }

    private void doitFunc(Linear.Function f) {
        String funName = f.name();
        if (funName.equals("main"))
            funName = funName+"0";
        gFuncName = funName;

        emitWithTab(".data");
        emit(funName+"_name:");
        emitWithTab(".string "+"\""+funName+"\"");

        emitWithTab(".text");
        emitWithTab(".globl "+funName);
        emit(funName+":");
        // prologue
        emitWithTab("pushq\t%rbp");
        emitWithTab("movq\t%rsp, %rbp");
        f.stms().forEach(this::doitStm);
        // should have "return" in its body
    }

    private void doit0(Linear.Program prog) throws Exception {
        try (OutputStreamWriter writer0 = new OutputStreamWriter(new FileOutputStream(fileName))) {
            writer = writer0;
            prog.funcs().forEach(this::doitFunc);

            // a main function
            emitWithTab(".globl main");
            emit("main:");
            // prologue
            emitWithTab("pushq\t%rbp");
            emitWithTab("movq\t%rsp, %rbp");
            emitWithTab("leaq\ttopHandler(%rip), %rdi");
            emitWithTab("callq\texn_frame_push");
            emitWithTab("callq\tmain0");
            emitWithTab("callq\texn_frame_pop");
            emitWithTab("leave");
            emitWithTab("ret");
            emitWithTab("\n");

            writer.write("\t.section .note.GNU-stack\n");
        }
    }

    public void doit(Linear.Program prog) {
        try {
            doit0(prog);
        }catch (Exception e){
            throw new AssertionError(e);
        }
    }
}
