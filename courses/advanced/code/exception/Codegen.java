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
            writer.write(STR."\t\{s}\n");
        } catch (IOException e) {
            throw new AssertionError(e);
        }
    }

    private void emitWithTab(String s) {
        emit(STR."\t\{s}");
    }

    private void doitStm(Linear.Stm.T stm) {
        switch (stm) {
            case Linear.Stm.Call(String f) -> {
                emitWithTab(STR."callq\t\{f}");
            }
            case Linear.Stm.Jmp(String l) -> {
                emitWithTab(STR."jmp\t\{l}");
            }
            case Linear.Stm.Label(String l) -> {
                emit(STR."\{l}:");
            }
            case Linear.Stm.Print(int n) -> {
                emitWithTab(STR."movq\t$\{n}, %rdi");
                emitWithTab(STR."callq\tprint");
            }
            case Linear.Stm.PopExnFrame() -> {
                emitWithTab(STR."callq\texn_frame_pop");
            }
            case Linear.Stm.PushExnFrame(String l) -> {
                emitWithTab(STR."leaq\t\{l}(%rip), %rdi");
                emitWithTab(STR."callq\texn_frame_push");
            }
            case Linear.Stm.Resume() -> {
                emitWithTab(STR."callq\texn_frame_pop");
                emitWithTab(STR."leaq\t\{gFuncName}_name(%rip), %rdi");
                emitWithTab(STR."callq\tcleanup");
                emitWithTab(STR."callq\texn_frame_pop");
                emitWithTab(STR."movq\t%rax, 8(%rbp)");
                emitWithTab(STR."// restore context");
                emitWithTab(STR."leave");
                emitWithTab(STR."ret");
            }
            case Linear.Stm.Return() -> {
                emitWithTab(STR."callq\texn_frame_pop");
                emitWithTab(STR."// restore context");
                emitWithTab(STR."leave");
                emitWithTab(STR."ret");
            }
            case Linear.Stm.Throw() -> {
                emitWithTab(STR."call throw0");
                emitWithTab(STR."jmp\t*%rax");
            }
        }
    }

    private void doitFunc(Linear.Function f) {
        String funName = f.name();
        if (funName.equals("main"))
            funName = STR."\{funName}0";
        gFuncName = funName;

        emitWithTab(STR.".data");
        emit(STR."\{funName}_name:");
        emitWithTab(STR.".string \"\{funName}\"");

        emitWithTab(STR.".text");
        emitWithTab(STR.".globl \{funName}");
        emit(STR."\{funName}:");
        // prologue
        emitWithTab(STR."pushq\t%rbp");
        emitWithTab(STR."movq\t%rsp, %rbp");
        f.stms().forEach(this::doitStm);
        // should have "return" in its body
    }

    private void doit0(Linear.Program prog) throws Exception {
        try (OutputStreamWriter writer0 = new OutputStreamWriter(new FileOutputStream(fileName))) {
            writer = writer0;
            prog.funcs().forEach(this::doitFunc);

            // a main function
            emitWithTab(STR.".globl main");
            emit(STR."main:");
            // prologue
            emitWithTab(STR."pushq\t%rbp");
            emitWithTab(STR."movq\t%rsp, %rbp");
            emitWithTab(STR."leaq\ttopHandler(%rip), %rdi");
            emitWithTab(STR."callq\texn_frame_push");
            emitWithTab(STR."callq\tmain0");
            emitWithTab(STR."callq\texn_frame_pop");
            emitWithTab(STR."leave");
            emitWithTab(STR."ret");
            emitWithTab(STR."\n");

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
