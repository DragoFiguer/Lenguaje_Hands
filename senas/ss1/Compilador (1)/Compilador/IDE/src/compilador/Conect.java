/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compilador;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.scene.control.TextArea;
import javax.swing.JTextArea;
/**
 *
 * @author michael
 */
public class Conect extends Thread{
    public JTextArea txt;
    public String str= "";
    BufferedWriter writer;
    BufferedReader reader;
    String res;
    
    public Conect(JTextArea txt){
        this.txt = txt;
        this.txt.addKeyListener(new KeyListener() {
            //private String str;
            @Override
            public void keyTyped(KeyEvent e) {
            }

            @Override
            public void keyPressed(KeyEvent e) {
                str += Character.toString(e.getKeyChar());
                if (e.getKeyChar() == KeyEvent.VK_ENTER){
                    try {
                        writer.write(str);
                        writer.flush();
                        str="";
                    } catch (Exception ex) {
                        System.out.println("Error Conect");
                        System.err.println(ex.getMessage());
                    }
                }
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });
        
        
    }
    @Override
    public void run(){
        System.out.println("Ya inicio");
        try {
            ProcessBuilder builder =  new ProcessBuilder("python","-u","C:\\Users\\michael\\Documents\\sem8\\Blanca\\Compilador\\Maquina.py");
            Process p = builder.start();
            
             if (p.isAlive()) {
                 System.out.println("VIVO");
            }else{
                 System.out.println("MUERTO");
            }
            /*Runtime exec = Runtime.getRuntime();
            Process comando = null;
            try {                
                //comando = exec.exec("python ..\\ArbolGramatical.py ");                
                comando = exec.exec("python ..\\Maquina.py ");                
            } catch (IOException ex) {
                Logger.getLogger(Editor.class.getName()).log(Level.SEVERE, null, ex);
            }*/
            
            reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            writer = new BufferedWriter(new OutputStreamWriter(p.getOutputStream()));
            
            res = reader.readLine();
            while(res != null){
                System.out.println(p.isAlive());
                if("cin>>".equals(res)){
                    //txt.setText(txt.getText()+ res + "\n");
                    txt.append(res+ "\n");
                    int tam = txt.getDocument().getLength();
                    txt.setCaretPosition(tam);
                    res = reader.readLine();
                }else{
                    //txt.setText(txt.getText()+ res + "\n");
                    txt.append(res+ "\n");
                    int tam = txt.getDocument().getLength();
                    txt.setCaretPosition(tam);
                    res = reader.readLine();                   
                }
            }
        } catch (IOException ex) {
            System.err.println(ex.getMessage());
        } catch (Throwable ex) {
            Logger.getLogger(Conect.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}