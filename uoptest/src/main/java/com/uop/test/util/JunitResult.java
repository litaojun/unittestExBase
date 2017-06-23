package com.uop.test.util;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

//import com.frame.test.thread.TestResultInfaces;

//import com.frame.test.thread.TestResultInfaces;

public class JunitResult {
	private static long signnum = 1122332122L;
	private  Lock lock=new ReentrantLock();
	private  Condition condition_con=lock.newCondition();
	private int status = 0;
	private int totalNum=0;
	private int sucessNum=0;
	private int failNum=0;
	private int exceptionNum=0;
	private int intfaceNum=0;
	private ArrayList<TestResultInfaces> trdlist = new ArrayList<TestResultInfaces>();
	private HashMap<String,JunitFaceResult> hmapResult = new HashMap<String,JunitFaceResult>();
	private ArrayList<String[]> sucesslist =new ArrayList<String[]>(),falllist=new ArrayList<String[]>(),exceptionlist=new ArrayList<String[]>();

	public void addJunitFaceResult(JunitFaceResult jfe)
	{
		this.hmapResult.put(jfe.getFacename(), jfe);
	}
	public ArrayList<TestResultInfaces> getTrdlist()
	{
		return this.trdlist;
	}
	public void setTrdlist(TestResultInfaces trd)
	{
		this.trdlist.add(trd);
	}
	public int getIntfaceNum()
	{
		return this.intfaceNum;
	}
	public void setIntfaceNum(int num)
	{
		this.intfaceNum = num;
	}
	public void setStatus(int s)
	{
		this.status =  s;
	}
	public int getStatus()
	{
		return this.status;
	}

	public void setTotalNum(int num)
	{
		this.totalNum = num;
	}
	public void setSucessNum(int num)
	{
		this.sucessNum = num;
	}
	public void setFailNum(int num)
	{
		this.failNum = num;
	}
	public int getTotalNum()
	{
		return this.totalNum;
	}
	public int getSucessNum()
	{
		return this.sucessNum;
	}
	public int getFailNum()
	{
		return this.failNum;
	}
	public int getExceptionNum()
	{
		return this.exceptionNum;
	}
	public void writeTestResult(String resultpath) throws IOException
	{
		Iterator<String> itr = hmapResult.keySet().iterator();
		while(itr.hasNext())
		{
			String infacename = itr.next();
			JunitFaceResult jfrlt = hmapResult.get(infacename);
			jfrlt.writeXML(String.format(resultpath, new String[]{infacename}));
		}
	}
}
