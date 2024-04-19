class Main{
    public static void main (String... args){
        try{
            System.out.println(11);
            try{
                System.out.println (21);
            }
            catch(Exception e){
                System.out.println (22);
            }
        }
        catch(Exception e){
             System.out.println (12);
        }
    }

    public void f(){
        try{
            System.out.println (21);
        }
        catch(Exception e){
            System.out.println (22);
        }
        finally{
            System.out.println (23);
        }
    }   
}
