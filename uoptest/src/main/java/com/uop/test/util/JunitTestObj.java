package com.uop.test.util;

import java.io.IOException;

import org.junit.casemsgr.TestCaseStyle;
import org.junit.casemsgr.TestManageContorl;

//import com.frame.test.core.TestManageContorl;
//import com.frame.test.util.TestCaseStyle;

public abstract class JunitTestObj {
	  private String caseidstr;
	    private TestCaseStyle tcs;
	    static{
	    	TestManageContorl tcl;
			try {
				tcl = new TestManageContorl();
//				tcl.tsmanager.addTestCase("D:\\litaojun\\测试用例\\测试用例.xlsx","useradd",13);
//				tcl.tsmanager.addTestCase("D:\\litaojun\\测试用例\\测试用例.xlsx","userlogin",6);
//				tcl.tsmanager.addTestCase("/home/testcase/tasecase.xlsx","useradd",13);
//				tcl.tsmanager.addTestCase("/home/testcase/tasecase.xlsx","userlogin",6);
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	    	
	    	
	    }
	    public TestCaseStyle getTestCaseStyle()
	    {
	    	return this.tcs;
	    }
	    public JunitTestObj(String caseid)
	    {
	    	try {
				TestManageContorl a = new TestManageContorl();
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	       this.caseidstr = caseid;
	       this.tcs = TestManageContorl.tsmanager.caseidMap.get(caseid);
	       
	    }
	    
	    public abstract  Object getTestImpData(Class c) ;
//	    {
//	    	Object o = c.newInstance();
//	    	return o;
//	    }
	    public abstract  Object getTestExpectedData(Class c) ;
}
