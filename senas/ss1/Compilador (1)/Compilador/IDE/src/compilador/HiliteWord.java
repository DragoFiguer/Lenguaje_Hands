/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compilador;

/**
 *
 * @author michael
 */
public class HiliteWord {
    int _position;  
    String _word;
    int _type;

    public HiliteWord(String word, int position, int type) {
        _position = position;   
        _word = word;
        _type=type;
    }
}
