import java.net.InetAddress;
//import osc.JavaOSC.modules.core.src.main.java.com.illposed.osc.*;
//import JavaOSC.modules.core.src.main.java.com.illposed.osc.*;
//import JavaOSC.modules.core.src.main.java.com.illposed.osc.utility.*;

public class Arms {


    private int[] v;
    private int G;
    private int D;
    private final int activeCount = 4; // in order to allow for drone vadi arms
    public Arms(int G, int D) {
        this.G = G;
        this.D = D;
        v = new int[4];
        for (int i = 0; i < 4; i++) {
            v[i]= (int) ((G/4 * i) + G/8) ;
        }


    }
    public Arms( int G, int D, int[] v) {
    this.G = G;
    this.D = D;
    setState(v);
    }

    public void setState(int[] v) {
        if (!setStte(v)) {
        System.out.print("BAD STATE:\t"+toString()+" ==>> " );
        for (int vs: v) {
            System.out.print(vs + ", ");
        }
        System.out.println("");
        } else {
          /*  InetAddress add = InetAddress.getLocalHost(); //update with shimone
            OSCMessage message = new OSCMessage(add.toString());
            message.addArgument(v);
            OSCPortOut out = new OSCPortOut(add);
            out.send(message);

        */

        }

    }

    public int[] getState() {
        return v;
    }
    public boolean isValidChange(int index, int pos){
       // System.out.println("" + Math.abs(this.v[index] - pos) + " < " + D);
        return Math.abs(this.v[index] - pos) < D;
    }//FIXED:debug this (allowing changes form 41 to 1 when D is 2
    public boolean setStte( int[] v) {
        //System.out.println("SETTINGSTATE");
        if(v.length != 4) {
            return false;
        }
        if(v[0] < v[1] && v[1] < v[2]  && v[2] < v[3] && v[3] < G) {
             for(int i = 0; i < v.length; i++) {

                if(!isValidChange(i, v[i])) return false;
             }
             this.v = v;
             return true;
        } else {
             return false;
        }
    }

    public String toString() {
    String r = "";
    r+="{";
    for (int i = 0; i < v.length - 1; i++) {
        r+= v[i] + ", ";
    }
    return r + v[v.length - 1] + "}";
    }
}
