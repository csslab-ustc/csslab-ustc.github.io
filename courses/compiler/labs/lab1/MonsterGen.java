public class MonsterGen {
    public static void print(String s) {
        System.out.print(s);
    }

    public static void usage() {
        print("Monster generator.\nUsage: java MonsterGen <num>");
        System.exit(1);
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1)
            usage();

        int n = Integer.parseInt(args[0]);

        print("""
                class Monster{
                    static void main(String[] args){
                        System.out.println(new Foo().foo());
                    }
                }

                class Foo{
                    public int foo(){
                        int sum = 0;
                """);
        for (int i = 0; i < n; i++)
            print("\t\tsum = sum + 1;\n");
        print("\t\treturn sum;\n");
        print("\t}\n");
        print("}\n\n");
    }
}

