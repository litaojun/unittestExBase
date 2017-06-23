package com.uop.test.util;

import java.util.HashMap;

public class TestCaseStyle 
{
	private String caseid; //用例编号
    private String functionPoint;  //功能点
    private String testPoint; //测试点
    private String preConditions;// 预制条件
    private String opeSteps;  //操作步骤
    private String inputData; //输入数据
    private String expectedResult;//期望结果
    private String retData;//返回数据
    private String testResult;//实际结果
    public boolean cmpcsid(String mbcid)
    {
    	boolean rs = this.caseid.equals(mbcid);
    	return rs;
    }
    public void setTestResult(String ret)
    {
    	this.testResult = ret;
    }
    public void setRetData(String ret)
    {
    	this.retData = ret;
    }
    public String getRetData()
    {
    	return this.retData;
    }

    public String getTestResult()
    {
    	return this.testResult;
    }
    public void setExpectedResult(String expectrst)
    {
    	this.expectedResult = expectrst;
    }
    
    public TestCaseStyle(String[] a)
    {
//    	inputData =new HashMap();
//    	preData = new HashMap();
    	iniData(a);
    }
    public TestCaseStyle() {
		// TODO Auto-generated constructor stub
	}
	public void iniData(String[] a)
    {
    	this.caseid = a[0];
    	this.functionPoint  =a[1];
    	this.testPoint = a[2];
    	this.preConditions = a[3];
    	this.opeSteps = a[4];
    	this.inputData =   a[5];
    	this.expectedResult = a[6];
    	
    	
    }
    public String getFunctionPoint()
    {
    	return this.functionPoint;
    }
    public String getCaseid()
    {
    	return this.caseid;
    }
    public String getTestPoint()
    {
    	return this.testPoint;
    }
    public String getPreConditions()
    {
    	return this.preConditions;
    }
    public String getOpeSteps()
    {
    	return this.opeSteps;
    }
    public String getInputData()
    {
    	return this.inputData;
    }
    public String getExpectedResult()
    {
    	return this.expectedResult;
    }
    public void setCaseid(String a)
    {
    	this.caseid = a;
    }
    public void setFunctionpoint(String a)
    {
    	this.functionPoint = a;
    }
    public void setTestpoint(String a)
    {
    	this.testPoint = a;
    }
    public void setPreconditions(String a)
    {
    	this.preConditions = a;
    }
    public void setOpesteps(String a)
    {
    	this.opeSteps = a;
    }
    public void setInputdata(String a)
    {
    	this.inputData = a;
    }
    public void setExpectedresult(String a)
    {
    	this.expectedResult = a;
    }
    public void setRetdata(String a)
    {
    	this.retData = a;
    }
    public void setTestresult(String a)
    {
    	this.testResult = a;
    }
//    public String getPreData()
//    {
//    	return this.preData;
//    }
//    public void iniData(String[] a)
//    {
//    	if(a==null || a.length != 7)
//    		return;
//    	functionPoint = a[0];
//    	preConditions = a[1];
//    	opeSteps = a[2];
////    	System.out.println("a[0]="+a[0]);
////    	System.out.println("a[1]="+a[1]);
////    	System.out.println("a[2]="+a[2]);
////    	System.out.println("a[3]="+a[3]);
//    	String[] temp = a[3].split("\n");
//    	for(int i=0;i<temp.length;i++)
//    	{
//    		//System.out.println("i="+i+";temp="+temp[i]);
//    		String aa = temp[i].split("=")[0];
//    		String bb = temp[i].split("=")[1];
//    		//System.out.println("aa="+aa+" ;bb="+bb);
//    		inputData.put(aa,bb);
//    	
//    	}
//    	expectedResult =  a[4].split("\n");
//    	temp = a[5].split("\n");
//    	for(int i=0;i<temp.length;i++)
//    	{
//    		preData.put(temp[i].split("=")[0], temp[i].split("=")[1]);
//    	}
//    	testResult = a[6];
//    }
//    public String toString()
//    {
//        String a= inputData.toString();
//        String b =preData.toString();
//        return a+b;
//    }
//    public Object[] traveToDataArray()
//    {
//    	Object[] a=new Object[4];
//    	a[0]=inputData.get("code").toString();
//    	a[1]=inputData.get("type").toString();
//    	//a[2]=preData.get("errcode");
//    	if(preData.get("errcode") == null)
//    		a[2]=null;
//    	else
//    		a[2]=preData.get("errcode").toString();
//    	a[3]=Integer.parseInt(preData.get("retcode").toString());
//    	//System.out.println("a[0]="+a[0]+";;a[1]="+a[1]+";;a[2]="+a[2]+";;a[3]="+a[3]);
//    	return a;
//    }
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
