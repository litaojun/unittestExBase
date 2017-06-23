package com.uop.test.util;

import org.junit.runner.Description;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import org.junit.runner.notification.RunListener;

public class JunitRunListener extends RunListener 
{
	JunitFaceResult junitResult =null;
//	 public void testSuiteStarted(Description description) throws Exception 
//	 {
//		 if(this.junitResult.getFacename()!=null && !this.junitResult.getFacename().equals(""))
//		       this.junitResult.setFacename(description.getDisplayName());
//	   }
	public JunitRunListener(JunitFaceResult junitResult)
	{
		this.junitResult = junitResult;
		
	}
    public void testRunStarted(Description description1)
            throws Exception
        {
    	  
        }

        public void testRunFinished(Result result1)
            throws Exception
        {
        	this.junitResult.addEnd();
        }

        public void testStarted(Description description1)
            throws Exception
        {
        }

        public void testFinished(Description description1)
            throws Exception
        {
        	this.junitResult.addSucess(description1.getDisplayName());
        }

        public void testFailure(Failure failure1)
            throws Exception
        {
        	String msg = failure1.getMessage();
        	String err = failure1.getTrace();
        	String exception = failure1.getException().getMessage();
        	System.out.println(String.format("msg=%s,err=%s,excepiton=%s", new String[]{msg,err,exception}));
        	this.junitResult.addFail(failure1.getDescription().getDisplayName(), new String[]{msg,err,exception});
        }

        public void testAssumptionFailure(Failure failure1)
        {
        }

        public void testIgnored(Description description1)
            throws Exception
        {
        }
}
