package com.uop.test.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class FileOperator {
    public static ArrayList<String> readFileByLines(String fileName) {  
    	ArrayList<String> retarryls = new ArrayList<String>();
        File file = new File(fileName);  
        BufferedReader reader = null;  
        try {  
           // System.out.println("以行为单位读取文件内容，一次读一整行：");  
           // reader = new BufferedReader(new FileReader(file));  
            reader = new BufferedReader(new InputStreamReader(new FileInputStream(fileName),"UTF-8"));  
            String tempString = null;  
            int line = 1;  
            // 一次读入一行，直到读入null为文件结束  
            while ((tempString = reader.readLine()) != null) {  
                // 显示行号  
            	//String utfstr =  new String(tempString.getBytes("UTF-8"));
                //System.out.println("line " + line + ": " + tempString); 
                retarryls.add(tempString);
                line++;  
            }  
            reader.close();  
        } catch (IOException e) {  
            e.printStackTrace();  
        } finally {  
            if (reader != null) {  
                try {  
                    reader.close();  
                } catch (IOException e1) {  
                }  
            }  
        }  
        return retarryls;
    }  
    public static void main(String[] args)
    {
    	FileOperator.readFileByLines("D:\\litaojun\\ulmenv\\testFrameManager\\target\\classes\\configcasepath.properties");
    }
}
