package com.uop.test.junit;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

//import org.junit.casemsgr.TestManageContorl;
import org.junit.runner.manipulation.CaseIdFilter;
import org.junit.runner.notification.RunNotifier;
import org.junit.runners.ParamSyncSuite;

import com.uop.test.util.JunitFaceResult;
import com.uop.test.util.JunitResult;
import com.uop.test.util.JunitRunListener;
import com.uop.test.util.TestManageContorl;


//import com.frame.test.junit.result.JunitFaceResult;
//import com.frame.test.junit.result.JunitResult;
//import com.frame.test.junit.result.JunitRunListener;
//import com.frame.util.TestManageContorl;

public class TestJunit {
	public static void main(String[] args) throws Exception
    {
	    JunitResult jrt = new JunitResult();
    	TestManageContorl tcl = new TestManageContorl();
    	HashMap<String,ArrayList<String[]>> casehmap = tcl.tsmanager.getCasehashmap();
    	Iterator<String> itr = casehmap.keySet().iterator();
    	RunNotifier notifier = new RunNotifier();
    	while(itr.hasNext())
    	{
    		String infacename = itr.next();
    		System.out.println("接口==========="+infacename);
    	    ArrayList<Object> caselsa = new ArrayList<Object>();
    	    ArrayList<String[]> casels = casehmap.get(infacename);
    	    for(String[] caseid:casels)
    	    {
    	    	caselsa.add(caseid[0]);
    	    }
    	    //CaseIdFilter a = new CaseIdFilter((String)test.getParameters().get(0))
    	    // ParamSyncSuite pzd = ParamSyncSuite.createParamSyncSuite(hmap.get(infacename), caselsa, infacename);
    	    Class x = tcl.tsmanager.hmap.get(infacename);
    	    ParamSyncSuite pzd = ParamSyncSuite.createParamSyncSuite(tcl.tsmanager.hmap.get(infacename), caselsa, infacename);
    		JunitFaceResult jfrsult = new JunitFaceResult(jrt);
    		JunitRunListener a = jfrsult.createJunitRunListener();
    		jfrsult.setFacename(infacename);
    		notifier.addListener(a);
    		pzd.run(notifier);
    		notifier.removeListener(a);
    		jrt.addJunitFaceResult(jfrsult);

    	}
    	System.out.println("args[0]="+args[0]);
    	jrt.writeTestResult(args[0]);
   	//jrt.writeTestResult("d://TEST-user.%s.xml");
    	//jrt.writeTestResult("/opt/jenkins/portal/junitresult/TEST-user.%s.xml");
    	 
    }
}
