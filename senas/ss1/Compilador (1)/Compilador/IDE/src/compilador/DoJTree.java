/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compilador;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreePath;

/**
 *
 * @author michael
 */
public class DoJTree {
    
    public DefaultTreeModel arbol() throws FileNotFoundException, IOException {
        File archivo = new File(".\\CodigoSintaxis.txt");
        FileReader fr = new FileReader(archivo);
        BufferedReader br = new BufferedReader(fr);
        String linea = br.readLine();
        // Construccion del arbol

        DefaultMutableTreeNode raiz = new DefaultMutableTreeNode(linea);
        DefaultTreeModel inicioArbol = new DefaultTreeModel(raiz);
        ArrayList<DefaultMutableTreeNode> padres = new ArrayList<>();
        padres.add(raiz);

        if (linea != null) {
            linea = br.readLine();
        }
        int i = 0;
        while (linea != null) {
            DefaultMutableTreeNode nuevo = new DefaultMutableTreeNode(linea);
            while (linea.charAt(i) == ' ') {
                i++;
            }
            if (i < padres.size()) {
                padres.remove(i);
            }
            padres.add(i, nuevo);
            inicioArbol.insertNodeInto(nuevo, padres.get(i - 1), (padres.get(i - 1)).getChildCount());

            i = 0;
            linea = br.readLine();
        }

        JTree tree = new JTree(inicioArbol);

        setTreeState(tree, tree.getPathForRow(0), true);
        
        return inicioArbol;
    }
    
    public DefaultTreeModel arbolSemantica() throws FileNotFoundException, IOException {
        File archivo = new File(".\\CodigoSemantica.txt");
        FileReader fr = new FileReader(archivo);
        BufferedReader br = new BufferedReader(fr);
        String linea = br.readLine();
        // Construccion del arbol

        DefaultMutableTreeNode raiz = new DefaultMutableTreeNode(linea);
        DefaultTreeModel inicioArbol = new DefaultTreeModel(raiz);
        ArrayList<DefaultMutableTreeNode> padres = new ArrayList<>();
        padres.add(raiz);

        if (linea != null) {
            linea = br.readLine();
        }
        int i = 0;
        while (linea != null) {
            DefaultMutableTreeNode nuevo = new DefaultMutableTreeNode(linea);
            while (linea.charAt(i) == ' ') {
                i++;
            }
            if (i < padres.size()) {
                padres.remove(i);
            }
            padres.add(i, nuevo);
            inicioArbol.insertNodeInto(nuevo, padres.get(i - 1), (padres.get(i - 1)).getChildCount());

            i = 0;
            linea = br.readLine();
        }

        JTree tree = new JTree(inicioArbol);

        setTreeState(tree, tree.getPathForRow(0), true);
        
        return inicioArbol;
    }

    public static void setTreeState(JTree tree, boolean expanded) {
        Object root = tree.getModel().getRoot();
        setTreeState(tree, new TreePath(root), expanded);
    }

    public static void setTreeState(JTree tree, TreePath path, boolean expanded) {
        Object lastNode = path.getLastPathComponent();
        for (int i = 0; i < tree.getModel().getChildCount(lastNode); i++) {
            Object child = tree.getModel().getChild(lastNode, i);
            TreePath pathToChild = path.pathByAddingChild(child);
            setTreeState(tree, pathToChild, expanded);
        }
        if (expanded) {
            tree.expandPath(path);
        } else {
            tree.collapsePath(path);
        }

    }
}
