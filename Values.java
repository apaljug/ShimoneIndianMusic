
import java.util.TimerTask;
import java.util.Timer;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
/**
 Write a simple code (in any language) for the following.
Print the values of four positive integer variables V1, V2, V3 and V4 iteratively every T milliseconds.
V1 < V2 < V3 < V4 < a given integer G. ('<' represents 'less than'.)
The difference between a variable's values in consecutive iterations < a given difference D.
In the i-th iteration, one of the variables must the value M*i+C, where M and C are given integers.
@version 1.1
*/
public class Values extends TimerTask {

    public static Arms positions;
    public static int i=0;
    static int T, G, D, M, C;
    public static int[] input = {20, 0,32, 0,31,29,27, 0,
           24,25,22,24,27, 0,25, 0,
           24, 0, 0, 0, 0, 0,22, 0,
           19, 0,22, 0,20, 0, 0, 0,
           20, 0,32, 0,31,29,27, 0,
           24,25,22,24,27, 0,25, 0,
           24, 0, 0, 0, 0, 0,22, 0,
           19, 0,22, 0,20, 0, 0, 0,
           24, 0,24,25,22, 0,24, 0,
           27, 0, 0, 0,24, 0,27, 0,
           29,31,32, 0,29, 0,30, 0,
           29, 0,27,29,27,25,24, 0,
           0, 0,24,25, 0,22, 0,24,
           27, 0, 0, 0,24, 0,27, 0,
           29,31,32,31,29,30,29,27,
           24,25,22,24,27,25,24,22} ;
    public void run() {
        // int pos = (M* i + C ) % G ;
        int pos = input[i];
        moveNearest(pos);
        System.out.println(positions.toString() + ""+i);
        i++;
    }

    public static void moveNearest(int pos) {
    int[] v = new int[positions.getState().length];

    System.arraycopy(positions.getState(), 0, v ,0 ,positions.getState().length);

    int low = G;
    int index = 0;
    for (int i = 0; i < v.length; i++) {
        int dif = Math.abs(pos - v[i]);
        if (dif < low) {
        low = dif;
        index = i;
        }
    }
    v[index] = pos;
    positions.setState(v);
    }


    /** args contains 4 integer values (in following order)
    T for clock seperation
    G for values max  (48)
    D for values seperation per (calculated)
    M another given integer
    C another given integer
    */
    public static void main(String[] args) throws FileNotFoundException {
    if( args.length < 5) {
        T = 200;
    G = 48;
    D = 10;
    M = 10;
    C = 100;

    } else {
    T = Integer.parseInt(args[0]); //greater than 100
    G = Integer.parseInt(args[1]);
    D = Integer.parseInt(args[2]);// difference between iterations max
    M = Integer.parseInt(args[3]);
    C = Integer.parseInt(args[4]);
    }
    positions = new Arms(G,D);
    if( T < 100 ) T = 100;//ensures T is not faster than the robot


    D = (int)(48 * T/1000.0);
    if ( D > 48 ) {
         D = 48;
    } // autocalculate D based upon movin speed of arms (real data)

    System.out.println("T: " + T + "\nG: " + G + "\nD: " + D + "\nM: " + M +
                        "\nC: " + C);
    Timer timer = new Timer();
    timer.schedule(new Values(), 0, T);

    }


}
