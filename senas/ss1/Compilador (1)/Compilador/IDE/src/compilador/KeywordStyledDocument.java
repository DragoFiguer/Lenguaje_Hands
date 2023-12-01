/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compilador;
import java.util.ArrayList;
import java.util.List;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.Style;

/**
 *
 * @author michael
 */
public class KeywordStyledDocument extends DefaultStyledDocument {

    private static final long serialVersionUID = 1L;

    private static void cath() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
    private Style _defaultStyle;
    private Style _cwStyle;
    private Style _commStyle;
    private Style _numStyle;
    static boolean bandMulLi = false;

    public KeywordStyledDocument(Style defaultStyle, Style cwStyle, Style commStyle, Style numStyle) {
        _defaultStyle = defaultStyle;
        _cwStyle = cwStyle;
        _commStyle = commStyle;
        _numStyle = numStyle;
    }

    @Override
    public void insertString(int offset, String str, AttributeSet a) throws BadLocationException {
        super.insertString(offset, str, a);
        refreshDocument();
    }

    @Override
    public void remove(int offs, int len) throws BadLocationException {
        super.remove(offs, len);
        refreshDocument();
    }

    private synchronized void refreshDocument() throws BadLocationException {
        String text = getText(0, getLength());
        final List<HiliteWord> list = processWords(text);

        setCharacterAttributes(0, text.length(), _defaultStyle, true);
        for (HiliteWord word : list) {
            int p0 = word._position;
            if (word._type == 2) {
                setCharacterAttributes(p0, word._word.length(), _commStyle, true);
            } else if (word._type == 1) {
                setCharacterAttributes(p0, word._word.length(), _cwStyle, true);
            } else {
                setCharacterAttributes(p0, word._word.length(), _numStyle, true);
            }
        }
    }

    private static List<HiliteWord> processWords(String content) {
        content += " ";
        List<HiliteWord> hiliteWords = new ArrayList<HiliteWord>();
        int lastWhitespacePosition = 0;
        int lastCommPosition = 0;
        int lastNumPosition = 0;
        String word = "";
        String comm = "";
        String num = "";
        boolean band = false;
        char[] data = content.toCharArray();
        try {
            for (int index = 0; index < data.length; index++) {
                char ch = data[index];
                //Palabras reservadas
                if (String.valueOf(ch).matches("\\W")) {
                    lastWhitespacePosition = index;
                    band = true;
                    if (word.length() > 0) {
                        if (isReservedWord(word)) {
                            hiliteWords.add(new HiliteWord(word, (lastWhitespacePosition - word.length()), 1));
                        }
                        word = "";
                    }
                } else {
                    word += ch;
                }
                if (index == 0) {
                    band = true;
                }
                //Numeros
                if (Character.isDigit(ch)) {
                    if (index == 0) {
                        if (!Character.isLetter(data[index]) && band) {
                            lastNumPosition = index;
                            num += data[index];
                            index++;
                            while (index != data.length) {
                                if (data[index] == '.') {
                                    ch = data[index + 1];
                                    if (Character.isDigit(ch)) {
                                        num += data[index];
                                        index++;
                                        while (index != data.length) {
                                            if (Character.isDigit(data[index])) {
                                                num += data[index];
                                            } else {
                                                break;
                                            }
                                            index++;
                                        }
                                    } else{
                                        num = "";
                                    }
                                }
                                if (Character.isDigit(data[index])) {
                                    num += data[index];
                                    index++;
                                } else {
                                    index--;
                                    break;
                                }

                            }
                            hiliteWords.add(new HiliteWord(num, lastNumPosition, 3));
                            num = "";
                        } else {
                            band = false;
                        }
                    } else {
                        if (!Character.isLetter(data[index - 1]) && band) {
                            lastNumPosition = index;
                            num += data[index];
                            index++;
                            while (index != data.length) {
                                if (data[index] == '.') {
                                    ch = data[index + 1];
                                    if (Character.isDigit(ch)) {
                                        num += data[index];
                                        index++;
                                        while (index != data.length) {
                                            if (Character.isDigit(data[index])) {
                                                num += data[index];
                                            } else {
                                                break;
                                            }
                                            index++;
                                        }
                                    } else {
                                        num = "";
                                    }
                                }
                                if (Character.isDigit(data[index])) {
                                    num += data[index];
                                    index++;
                                } else {
                                    index--;
                                    break;
                                }
                            }
                            hiliteWords.add(new HiliteWord(num, lastNumPosition, 3));
                            num = "";
                        } else {
                            band = false;
                        }
                    }
                }
                //Comentarios de una linea
                if (index + 1 <= data.length) {
                    if (data[index] == '/' && data[index + 1] == '/') {
                        lastCommPosition = index;
                        while (index != data.length) {
                            if (data[index] == '\n') {
                                //index++;
                                break;
                            } else {
                                comm += data[index];
                            }
                            index++;
                        }
                        hiliteWords.add(new HiliteWord(comm, lastCommPosition, 2));
                        comm = "";
                    }
                }
                //Comentarios de varias lineas
                if (index + 1 <= data.length) {
                    if (data[index] == '/' && data[index + 1] == '*') {
                        lastCommPosition = index;
                        comm += data[index];
                        index += 2;
                        while (true) {
                            if (index + 1 <= data.length) {
                                if (data[index] == '*' && data[index + 1] == '/' || index == data.length) {
                                    index++;
                                    break;
                                } else {
                                    comm += data[index];
                                }
                                index++;
                            } else {
                                break;
                            }
                        }
                        comm += '*';
                        comm += '/';
                        comm += '/';
                        hiliteWords.add(new HiliteWord(comm, lastCommPosition, 2));
                        comm = "";
                    }
                }

            }
        } catch (Exception e) {
        }
        return hiliteWords;
    }

    private static final boolean isReservedWord(String word) {
        return (word.equals("main")
                || word.equals("if")
                || word.equals("then")
                || word.equals("else")
                || word.equals("do")
                || word.equals("while")
                || word.equals("repeat")
                || word.equals("until")
                || word.equals("cin")
                || word.equals("cout")
                || word.equals("real")
                || word.equals("int")
                || word.equals("break")
                || word.equals("end")
                || word.equals("boolean"));
    }
}
