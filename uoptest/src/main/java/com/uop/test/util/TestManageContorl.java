package com.uop.test.util;

import java.io.IOException;
import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

//import com.frame.test.junit.util.FileOperator;
//import com.frame.test.thread.TestResultData;
//import com.frame.test.util.AnnotationFilterClass;
//import com.frame.test.util.ClassUtils;
//import com.frame.test.util.IfsPreDeal;
//import com.frame.test.util.PreResultDeal;
//import com.frame.test.util.TestCaseManagr;


public class TestManageContorl 
{
    public static Map<String,MethodContext> interfacemethod = null;
    public static Map<String,MethodContext> resultmethod  = null;
    public static TestCaseManagr tsmanager = null;
    public static TestResultData trdata = null;
    public static void cleanTestResultData()
    {
    	trdata = new TestResultData();
    }
	 public TestManageContorl() throws ClassNotFoundException, IOException
	 {
		 if(tsmanager==null)
		 {
			 tsmanager = new TestCaseManagr();
			 ArrayList<String> patharray = FileOperator.readFileByLines("configcasepath.properties");
			 //ArrayList<String> patharray = FileOperator.readFileByLines("configcasepathwin.properties");
			 for(int i=0;i<patharray.size();i++)
			 {
				 String linestr = patharray.get(i);
				 String[] a = linestr.split(",");
				 tsmanager.addTestCase(a[1],a[0],Integer.valueOf(a[2]));
				 tsmanager.hmap.put(a[0], Class.forName(a[3]));
			 }
//			 tsmanager.addTestCase("D:\\litaojun\\测试用例\\测试用例.xlsx","useradd",13);
//			 tsmanager.addTestCase("D:\\litaojun\\测试用例\\测试用例.xlsx","userlogin",6);
//			 tsmanager.addTestCase("D:\\litaojun\\测试用例\\测试用例.xlsx","userdel",4);
//			 tsmanager.addTestCase("D:\\litaojun\\测试用例\\测试用例.xlsx","contentadd",21);
			 
//			 tsmanager.addTestCase("/home/testcase/tasecase.xlsx","useradd",13);
//			 tsmanager.addTestCase("/home/testcase/tasecase.xlsx","userlogin",6);
//			 tsmanager.addTestCase("/home/testcase/tasecase.xlsx","userdel",4);
//			 tsmanager.addTestCase("/home/testcase/tasecase.xlsx","contentadd",21);
		 }
		 if(trdata == null)
		 {
			 trdata = new TestResultData();
		 }
		// TestManageContorl.init();
	 }
	 public static TestCaseManagr getTestCaseManagr()
	 {

		 return tsmanager;
	 }
	 public static void init() throws ClassNotFoundException, IOException
	 {
		 if(TestManageContorl.interfacemethod == null)
		 {
			 TestManageContorl.interfacemethod = new HashMap<String,MethodContext>();
			 initInterfacemethod();
		 }
		 if(TestManageContorl.resultmethod == null)
		 {
			 TestManageContorl.resultmethod = new HashMap<String,MethodContext>();
			 initResultmethod();
		 }
	 }
	 public static Map<String,MethodContext> getInterfacemethod() throws ClassNotFoundException, IOException
	 {
		 if(interfacemethod==null)
			 TestManageContorl.init();
		 return interfacemethod;
	 }
	 public static Map<String,MethodContext> getResultmethod() throws ClassNotFoundException, IOException
	 {
		 if(resultmethod==null)
			 TestManageContorl.init();
		 return resultmethod;
	 }

     public static void initInterfacemethod() throws ClassNotFoundException, IOException
     {
    	 ArrayList<Class>  x = ClassUtils.filterClassByKey("Tran","com.frame.test.ifspdl");
    	 System.out.println("xxx="+x.size());
//    	 for(Class s : x)
//    		 System.out.println(s.getName());
    	 ArrayList<Method> als = AnnotationFilterClass.filterMethodListByAnnotation( x, IfsPreDeal.class);
    	 for(Method md:als)
    	 {
    		Annotation[] ans =  md.getAnnotations();
    		for(Annotation an:ans)
    		{
    			if(an instanceof IfsPreDeal)
    			{
    				IfsPreDeal tcs = (IfsPreDeal) an;
    				putInterfacemethod(tcs,md);
    				break;
    			}
    		}
    		 System.out.println(md.getName());
    	 }

     }
     public static void putInterfacemethod(IfsPreDeal tc,Method md)
     {
    	// System.out.println("putInterfacemethod="+md.getName()+"--class--"+md.getDeclaringClass());
    	 String ifname = tc.infname();
    	 MethodContext curmactch = new MethodContext(md);
    	 interfacemethod.put(ifname, curmactch);
//    	 if(interfacemethod.containsKey(ifname))
//    	 {
//    	 }
//    	 else
//    	 {
//    		 interfacemethod.put(ifname, curmactch);
//    	 }
     }
     
     public static void initResultmethod() throws ClassNotFoundException, IOException
     {
    	 ArrayList<Class>  x = ClassUtils.filterClassByKey("ResultMatch","com.frame.test");
    	// System.out.println("xxx="+x.size());
//    	 for(Class s : x)
//    		 System.out.println(s.getName());
    	 ArrayList<Method> als = AnnotationFilterClass.filterMethodListByAnnotation( x, PreResultDeal.class);
    	 for(Method md:als)
    	 {
    		Annotation[] ans =  md.getAnnotations();
    		for(Annotation an:ans)
    		{
    			if(an instanceof PreResultDeal)
    			{
    				PreResultDeal tcs = (PreResultDeal) an;
    				putResultComparemethod(tcs,md);
    				break;
    			}
    		}
    		 System.out.println(md.getName());
    	 }

     }
     public static void putResultComparemethod(PreResultDeal tc,Method md)
     {
    	// System.out.println("putResultComparemethod="+md.getName()+"--class--"+md.getDeclaringClass());
    	 String ifname = tc.infname();
    	 MethodContext curmactch = new MethodContext(md);
    	 resultmethod.put(ifname, curmactch);
     }
     
}
