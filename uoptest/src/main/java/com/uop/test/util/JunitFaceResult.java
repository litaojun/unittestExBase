package com.uop.test.util;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;

import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.OutputFormat;
import org.dom4j.io.XMLWriter;

public class JunitFaceResult {
	private int facestatus = 0;
	private int faceTotalNum=0;
	private int facesucess=0;
	private int facefail=0;
	private int faceexcepiton=0;
	private String facename;
	private ArrayList<String> sucesslist = new ArrayList<String>();
	private ArrayList<String> falllist= new ArrayList<String>();
	private ArrayList<String> exceptionlist = new ArrayList<String>();
	private HashMap<String,String[]> errlist = new HashMap<String,String[]>();
	private JunitResult junitResult;
	public JunitFaceResult(JunitResult jresult)
	{
		this.junitResult = jresult;
	}
	public void addEnd()
	{
		this.junitResult.addJunitFaceResult(this);
	}
	public void addSucess(String caseid)
	{
		if(!this.falllist.contains(caseid))
		{
			sucesslist.add(caseid);
			this.facesucess++;
			this.faceTotalNum++;
		}
	}
	public void addFail(String caseid,String[] err)
	{
		falllist.add(caseid);
		this.errlist.put(caseid, err);
		this.facefail++;
		this.faceTotalNum++;
	}
	public void addException(String caseid)
	{
		this.exceptionlist.add(caseid);
		this.faceexcepiton++;
		this.faceTotalNum++;
	}
	public void setFacestatus(int faceStatus)
	{
		this.facestatus = faceStatus;
	}
	public void setFaceTotalNum(int    faceTotalNum )
	{
		this.faceTotalNum = faceTotalNum;
	}
	public void setFacesucess(int    faceSucess)
	{
		this.facesucess = faceSucess;
	}
	public void setFacefail(int    faceFail)
	{
		this.facefail = faceFail;
	}
	public void setFaceexcepiton(int    faceExcepiton)
	{
		this.faceexcepiton = faceExcepiton;
	}
	public void setFacename(String facename)
	{
		this.facename = facename;
	}
	
	public int getFacestatus()  
	{
		return this.facestatus;
	}
	public int getFaceTotalNum() 
	{
		return this.faceTotalNum;
		
	}
	public int getFacesucess()   
	{
		return this.facesucess;
	}
	public int getFacefail()    
	{
		return this.facefail;
	}
	public int getFaceexcepiton()
	{
	    return this.faceexcepiton;	
	}
	public String getFacename()
	{
		return this.facename;
		
	}
	public JunitRunListener createJunitRunListener()
	{
		JunitRunListener jlr = new JunitRunListener(this);
		return jlr;
	}
	public void writeXML(String path) throws IOException
	{
		 Element root = DocumentHelper.createElement("testsuite"); 
		 root.addAttribute( "tests", String.valueOf(this.faceTotalNum) );
		 root.addAttribute( "failures", String.valueOf(this.facefail) );
		 root.addAttribute( "name",  String.valueOf(this.facename) );
		 root.addAttribute( "time",  String.valueOf(0) );
		 root.addAttribute( "errors",  String.valueOf(this.facefail) );
		 root.addAttribute( "skipped",  String.valueOf(0) );
         Document doucment = DocumentHelper.createDocument(root);  
         //根节点  
         for(int i=0;i<this.sucesslist.size();i++)
         {
             Element element1 = root.addElement("testcase");  
             element1.addAttribute( "classname", this.facename );  
             element1.addAttribute( "name",sucesslist.get(i) );  
             element1.addAttribute( "time", "0" ); 
         }
         for(int i=0;i<this.falllist.size();i++)
         {
             Element element1 = root.addElement("testcase");  
             element1.addAttribute( "classname", this.facename );  
             element1.addAttribute( "name",falllist.get(i) );  
             element1.addAttribute( "time", "0" ); 
             Element fail = element1.addElement("failure");
             String[] err = this.errlist.get(falllist.get(i));
             fail.addAttribute("message", err[0]);
             fail.addAttribute("type", "java.lang.AssertionError");
             fail.addText(err[1]);
         }
         OutputFormat format = new OutputFormat();  
         FileOutputStream file = new FileOutputStream(path);  
         XMLWriter xml = new XMLWriter(file);  
         xml.write(doucment);  
         xml.close();  
	}
	
	public static void main(String[] args) 
	{
		JunitResult jrt = new JunitResult();
		JunitFaceResult jfrsult = new JunitFaceResult(jrt);
		
//		jfrsult.setFaceTotalNum(10);
//		jfrsult.setFacesucess(5);
//		jfrsult.setFacefail(4);
//		jfrsult.setFaceexcepiton(1);
		jfrsult.setFacename("useradd");
		for(int i=0;i<5;i++)
		{
			jfrsult.addSucess(String.format("wst_%s", i));
		}
		for(int i=5;i<9;i++)
		{
			jfrsult.addFail(String.format("wst_%s", i),null);
		}
		//jfrsult.addException("wst_9");
		try {
			jfrsult.writeXML("d://TEST-useradd.wst_1.am.xml");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
