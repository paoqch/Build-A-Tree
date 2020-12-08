import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

//Server Timer class
public class Timer {
    JFrame window;
    JLabel counterLabel;
    Font font1 = new Font("Arial", Font.PLAIN,200);
    javax.swing.Timer timer;
    int second, minute;

    //Display method
    public static  void main(String[] args){
        new Timer();
    }
    public Timer(){
        window = new JFrame();
        window.setSize(800,600);
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setLayout(null);

        counterLabel = new JLabel();
        counterLabel.setBounds(300,50,200,100);
        counterLabel.setHorizontalAlignment(JLabel.CENTER);
        window.add(counterLabel);
        window.setVisible(true);

        //Timer mode in minutes and seconds
        second = 0;
        minute = 0;
        normalTimer();
        timer.start();
        System.out.println("Timer Started");
    }

    //Timer change from seconds to minutes
    public void normalTimer(){
        timer = new javax.swing.Timer(1000, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                second++;
                counterLabel.setText(minute + ":" + second);

                if(second == 60){
                    second = 0;
                    minute++;
                    counterLabel.setText(minute + ":" + second);
                }
            }
        });
    }
}