package com.uop.test.user.goods.config.test;

import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.util.HashMap;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonParseException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.casemsgr.TestCaseStyle;
import org.junit.runner.manipulation.TestCase;

import com.alibaba.fastjson.JSONObject;
import com.uop.test.user.goods.config.impl.GoodsDisplayImpl;
import com.uop.test.util.InterfaceConfig;
import com.uop.test.util.JunitTestObj;
import com.uop.test.util.SpringUtil;
import com.uop.test.util.TestSend;


public class UserPropImportTest extends JunitTestObj
{
	Log log=LogFactory.getLog(UserPropImportTest.class);
	
	private ObjectMapper objectMapper = new ObjectMapper();

	//public static String URL = "https://dev-api.opg.cn/prop/users";
	public static String URL = InterfaceConfig.userImportURL;
	public UserPropImportTest(String caseid) {
		super(caseid);
		// TODO Auto-generated constructor stub
	}
	
	@Test
	@TestCase(ifname = "bestvuserprop", cstype = 3,rule = {25,37,1}, cls = Class.class)
	public void testPropImport() throws JsonGenerationException, JsonMappingException, IOException, InterruptedException
	{
		log.error(String.format("接口=%s，测试用例ID=%s,method=%s", new String[] {this.getTestCaseStyle().getFunctionPoint(),this.getTestCaseStyle().getCaseid(),"testPropImport"}));
		log.error("UserPropImportTest--->testPropImport");
		//得到用例输入数据
		//发送测试请求
		String retjsonstr = TestSend.doGet(URL, null);
		log.error("接口返回数据==" + retjsonstr);
		Thread.sleep(5000);
		//接口返回码及数据格式比对对
		//boolean b = UserProImplBestvCompareRetcode.compareUserPropRetcodeDataGuid(uprinfo, expectedstr,retjsonstr,"bestvapp");
//		//DB数据比对
//		boolean a = UserPropImplBestvDB.compareUserPropDbData(uprinfo, expectedstr);
		//assertTrue(a);
		//assertTrue(b);
		log.error(String.format("接口=%s，测试用例ID=%s,结束", new String[] {this.getTestCaseStyle().getFunctionPoint(),this.getTestCaseStyle().getCaseid()}));
	}
	
	

	
	/*
	 * 
	* Title: getTestImpData
	* Description: 获取用例输入数据，并转换数据格式
	* @param c
	* @return 
	* @see com.frame.util.JunitTestObj#getTestImpData(java.lang.Class)
	 */
	public  Object getTestImpData(Class c)
	{
		GoodsDisplayImpl urp = null;
		TestCaseStyle tcs = this.getTestCaseStyle();
		String caseinputdata = tcs.getInputData();
		caseinputdata = caseinputdata.replaceAll("\r|\n", ",");
		caseinputdata = "{"+caseinputdata+"}";
		try {
			 urp = objectMapper.readValue(caseinputdata, GoodsDisplayImpl.class);
		} catch (JsonParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (JsonMappingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return urp;
		//return JSONObject.parseObject(caseinputdata);
	}
	/*
	 * 
	* Title: getTestExpectedData
	*Description: 获取用例预期结果数据，并转换数据格式
	* @param c
	* @return 
	* @see com.frame.util.JunitTestObj#getTestExpectedData(java.lang.Class)
	 */
	public   Object getTestExpectedData(Class c) 
	{
		TestCaseStyle tcs = this.getTestCaseStyle();
		String expectedStr = tcs.getExpectedResult();
		String[] a = expectedStr.split(":");
		return a[1];
	}
	public  String getTestImpDataStr(Class c)
	{
		TestCaseStyle tcs = this.getTestCaseStyle();
		String caseinputdata = tcs.getInputData();
		caseinputdata = caseinputdata.replaceAll("\r|\n", ",");
		caseinputdata = "{data:{"+caseinputdata+"}}";
		return caseinputdata;
		//return JSONObject.parseObject(caseinputdata);
	}
	
 static void main(String[] args) {
		// TODO Auto-generated method stub
        
	}

}
