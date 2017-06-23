package com.uop.test.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class TestResultData 
{
	public TestResultData()
	{
		
	}
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
	private ArrayList<String[]> sucesslist =new ArrayList<String[]>(),falllist=new ArrayList<String[]>(),exceptionlist=new ArrayList<String[]>();
	public void removeOneResultInfaces(String infacename)
	{
		lock.lock();
		for(TestResultInfaces t:this.trdlist)
		{
			if(t.getFacename().equals(infacename))
			{
				this.trdlist.remove(t);
				break;
			}
		}
		 ArrayList<String[]> tmp = new ArrayList<String[]>();
		for(String[] x:sucesslist)
		{
			
			if(x[1].equals(infacename))
				tmp.add(x);
		}
		sucesslist.removeAll(tmp);
		tmp = new ArrayList<String[]>();
		for(String[] y:falllist)
		{
			if(y[1].equals(infacename))
				tmp.add(y);
		}
		falllist.removeAll(tmp);
		tmp = new ArrayList<String[]>();
		for(String[] z:exceptionlist)
		{
			if(z[1].equals(infacename))
				tmp.add(z);
		}
		exceptionlist.removeAll(tmp);
		lock.unlock();
	}
	public void setTrdlistStatusEnd()
	{
		this.totalNum=0;
		this.failNum = 0;
		this.sucessNum = 0;
		this.exceptionNum =0;
		this.intfaceNum = 0;
		HashMap<String,Integer> sucesshm = new HashMap<String,Integer>();
		HashMap<String,Integer> failhm = new HashMap<String,Integer>();
		HashMap<String,Integer> exceptionhm = new HashMap<String,Integer>();
		for(String a[]:sucesslist)
		{
			this.totalNum++;
			this.sucessNum++;
			if(sucesshm.containsKey(a[1]))
			{
				int curint = sucesshm.get(a[1]);
				curint++;
				sucesshm.put(a[1], curint);
			}
			else
			{
				sucesshm.put(a[1], 1);
			}
		}
		for(String a[]:falllist)
		{
			this.totalNum++;
			this.failNum++;
			if(failhm.containsKey(a[1]))
			{
				int curint = failhm.get(a[1]);
				curint++;
				failhm.put(a[1], curint);
			}
			else
			{
				failhm.put(a[1], 1);
			}
		}
		for(String a[]:exceptionlist)
		{
			this.totalNum++;
			this.exceptionNum++;
			if(exceptionhm.containsKey(a[1]))
			{
				int curint = exceptionhm.get(a[1]);
				curint++;
				exceptionhm.put(a[1], curint);
			}
			else
			{
				exceptionhm.put(a[1], 1);
			}
		}
		for(TestResultInfaces x : this.trdlist)
		{
			String key = x.getFacename();
			int e=0,f=0,s=0,t=0;
			if(exceptionhm.containsKey(key))
			{
				e=exceptionhm.get(key);
			}
			x.setFaceexcepiton(e);
			if(failhm.containsKey(key))
			{
				f=failhm.get(key);
			}
			x.setFacefail(f);
			if(sucesshm.containsKey(key))
			{
				s=sucesshm.get(key);
			}
			x.setFacesucess(s);
			x.setFaceTotalNum(s+f+e);
			x.setFacestatus(2);
		}
		
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
	public void addNum(int ty,String caseid,String funstr)
	{
		lock.lock();
//		if(this.status!=2)
//		{
			//totalNum++;
			switch(ty)
			{
				case 0:
				{
					sucesslist.add(new String[]{caseid,funstr});
					//sucessNum++;
					break;
				}
				case 1:
				{
					falllist.add(new String[]{caseid,funstr});
					//failNum++;
					break;
				}
				case 2:
				{
					exceptionlist.add(new String[]{caseid,funstr});
					//exceptionNum++;
					break;
				}
			}
//		}
//		else
//		{
//			this.dealSection(ty, new String[]{caseid,funstr});
//		}
		lock.unlock();
	}
	public void dealSection(int ty,String[] objstr)
	{
		int i = 9;
		if(this.sucesslist.contains(objstr))
		{
			i=0;
			if(ty!=0)
			{
				this.sucesslist.remove(objstr);
				//this.sucessNum --;
			}
		}
		if(this.falllist.contains(objstr))
		{
			i=1;
			if(ty!=1)
			{
				this.falllist.remove(objstr);
				//this.failNum--;
			}
		}
		if(this.exceptionlist.contains(objstr))
		{
			i=2;
			if(ty!=2)
			{
				this.exceptionlist.remove(objstr);
				//this.exceptionNum--;
			}
		}
		if(i!=ty)
		{
			switch(ty)
			{
			case 0:
			{
					sucesslist.add(objstr);
					//sucessNum++;
				break;
			}
			case 1:
			{
				falllist.add(objstr);
				//failNum++;
				break;
			}
			case 2:
			{
				exceptionlist.add(objstr);
				//exceptionNum++;
				break;
			}
			}
		}
		
			
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
}
