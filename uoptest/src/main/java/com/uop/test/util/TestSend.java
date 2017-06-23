package com.uop.test.util;



import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;

import org.json.JSONException;
import com.alibaba.fastjson.JSONObject;

import com.google.common.collect.Lists;

import org.apache.http.Consts;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.NameValuePair;
import org.apache.http.ParseException;
import org.apache.http.message.BasicHeader;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;


//import com.alibaba.fastjson.JSONObject;
//import com.google.common.collect.Lists;

public abstract class TestSend 
{
	//public static String URL = "http://127.0.0.1:8080/prop/users";
	public static String URL = "https://dev-api.opg.cn/prop/users";
	public static String key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApwbuhLHGlRmJwFwnH07ubOMZ3BFuEnAiq+lRYGMZ5KznAO9p+ReEYU+smh/2FH94RRIDD0qi7Y29DfW0eUbhGiW7YV1dPtQ6obEeqBno2ZKNSKiwNfyq+1PQuZBtmv0PuJlPTdlWEBSVkC3F3Twhaqgvxpv9Sy8FotZr4Sd4KYTNaW+YKOF0R5phsOEU2lhnc1gSr2jBdXg91eYp70/nEhS3lFEPZNO7d3XObLfMVirJnrTUQKE3RBUB4OqYVJscTMazGy8wRz59ag9qPCHMhsF4iy+RmnfuLL7Ib94W1eQciQYMLLZHclnlGoiF8qDH0V8I8C/JZag9SkeyIav45wIDAQAB";
    public static void main(String[] args) throws JSONException 
    {
        JSONObject jsobj1 = new JSONObject();
        JSONObject jsobj2 = new JSONObject();
        jsobj2.put("uuid", "2111222111111221");
        jsobj2.put("moblieNo", "18916899931");
        jsobj2.put("name", "李涛军");
        jsobj2.put("status", "1");
        jsobj1.put("data", jsobj2);
        postJson(jsobj1,URL);

    }

    /*
     * post json
     */
    public static String postJson(JSONObject json,String url) 
    {

        CloseableHttpClient client = HttpClients.createDefault();
		//HttpClient client = new DefaultHttpClient();
        HttpPost post = new HttpPost(url);

        //post.addHeader("sign","e50a54777db445aed84627dbc5e83a5c4b209c3d740700f4f80bf2ce3f18bad8");
        String result = "";
        try {
            StringEntity s = new StringEntity(json.toString(), "utf-8");
//            s.setContentEncoding(new BasicHeader(HTTP.CONTENT_TYPE,
//                    "application/json"));
            byte[] a = new byte[1024] ;
            int len = s.getContent().read(a);
            //ystem.out.println("reqjsondata===="+new String(a));
            post.setEntity(s);
            // 发送请求
            HttpResponse httpResponse = client.execute(post);
            // 获取响应输入流
            InputStream inStream = httpResponse.getEntity().getContent();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inStream, "utf-8"));
            StringBuilder strber = new StringBuilder();
            String line = null;
            while ((line = reader.readLine()) != null)
                strber.append(line + "\n");
            inStream.close();
            result = strber.toString();
            //System.out.println(result);
            if (httpResponse.getStatusLine().getStatusCode() == HttpStatus.SC_OK)
            {
                    System.out.println("请求服务器成功，做相应处理");
            } else 
            {
                System.out.println("请求服务端失败");
            }
            

        } catch (Exception e) {
            System.out.println("请求异常");
            throw new RuntimeException(e);
        }

        return result;
    }

    /*
     * put json
     */
    public static String putJson(JSONObject json,String url) 
    {
        CloseableHttpClient client = HttpClients.createDefault();
		//HttpClient client = new DefaultHttpClient();
        HttpPut post = new HttpPut(url);
        String result = "";
        try {
            StringEntity s = new StringEntity(json.toString(), "utf-8");
//            s.setContentEncoding(new BasicHeader(HTTP.CONTENT_TYPE,
//                    "application/json"));
            byte[] a = new byte[1024] ;
            int len = s.getContent().read(a);
            //System.out.println("reqjsondata===="+new String(a));
            post.setEntity(s);
            // 发送请求
            HttpResponse httpResponse = client.execute(post);
            // 获取响应输入流
            InputStream inStream = httpResponse.getEntity().getContent();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inStream, "utf-8"));
            StringBuilder strber = new StringBuilder();
            String line = null;
            while ((line = reader.readLine()) != null)
                strber.append(line + "\n");
            inStream.close();
            result = strber.toString();
            //System.out.println(result);
            if (httpResponse.getStatusLine().getStatusCode() == HttpStatus.SC_OK)
            {
                    System.out.println("请求服务器成功，做相应处理");
            } else 
            {
                System.out.println("请求服务端失败");
            }
            

        } catch (Exception e) {
            System.out.println("请求异常");
            throw new RuntimeException(e);
        }

        return result;
    }


    /*
     * post
     */

	public static String doPost(HashMap<String,String> hmp)  
    {  
        String uriAPI = "http://10.205.33.248:9026/prop/users";//Post方式没有参数在这里  
        String result = "";  
        HttpPost httpRequst = new HttpPost(uriAPI);//创建HttpPost对象  
        Iterator<Entry<String, String>> itr = hmp.entrySet().iterator();
        List <NameValuePair> params = new ArrayList<NameValuePair>();  
        while(itr.hasNext())
        {
        	Entry<String, String> entry = itr.next();
        	
        	params.add(new BasicNameValuePair(entry.getKey(), entry.getValue()));
        }
          
        try {  
            httpRequst.setEntity(new UrlEncodedFormEntity(params,"UTF-8"));  
            HttpResponse httpResponse = HttpClients.createDefault().execute(httpRequst);  
            if(httpResponse.getStatusLine().getStatusCode() == 200)  
            {  
                HttpEntity httpEntity = httpResponse.getEntity();  
                result = EntityUtils.toString(httpEntity);//取出应答字符串  
            }  
        } catch (UnsupportedEncodingException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
            result = e.getMessage().toString();  
        }  
        catch (ClientProtocolException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
            result = e.getMessage().toString();  
        }  
        catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
            result = e.getMessage().toString();  
        }  
        return result;  
    }  
    
    public static String sendInfo(String sendurl, String data) {
    CloseableHttpClient client = HttpClients.createDefault();
    HttpPost post = new HttpPost(sendurl);
    StringEntity myEntity = new StringEntity(data,
            ContentType.APPLICATION_JSON);// 构造请求数据
    post.setEntity(myEntity);// 设置请求体
    String responseContent = null; // 响应内容
    CloseableHttpResponse response = null;
    try {
        response = client.execute(post);
        if (response.getStatusLine().getStatusCode() == 200) {
            HttpEntity entity = response.getEntity();
            responseContent = EntityUtils.toString(entity, "UTF-8");
        }
    } catch (ClientProtocolException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        try {
            if (response != null)
                response.close();

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (client != null)
                    client.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    return responseContent;
} 
    public static String doGet(String httpurl,HashMap<String,String> nvpair) throws ParseException, IOException
    {
    	
    	String result= "";
    	CloseableHttpClient client = HttpClients.createDefault();
    	
    	
    	String paramstr = "";
    	if(nvpair!=null)
    	{
    	    List<NameValuePair> params = Lists.newArrayList();
    	    Iterator<String> itr = nvpair.keySet().iterator();
    	    while(itr.hasNext())
    	    {
    	    	String key = itr.next();
    	    	params.add(new BasicNameValuePair(key,nvpair.get(key)));
    	    }
    	    paramstr = EntityUtils.toString(new UrlEncodedFormEntity(params, Consts.UTF_8));
    	    paramstr = "?"+paramstr;
    	}
    	HttpGet httpRequst = new HttpGet(httpurl + paramstr);

    	try {
   //使用DefaultHttpClient类的execute方法发送HTTP GET请求，并返回HttpResponse对象。
			HttpResponse httpResponse = client.execute(httpRequst);//其中HttpGet是HttpUriRequst的子类
		    if(httpResponse.getStatusLine().getStatusCode() == 200)
		    {
		    	HttpEntity httpEntity = httpResponse.getEntity();
		    	result = EntityUtils.toString(httpEntity);//取出应答字符串
		    // 一般来说都要删除多余的字符 
		    	result.replaceAll("\r", "");//去掉返回结果中的"\r"字符，否则会在结果字符串后面显示一个小方格  
		    }
                   else 
                        httpRequst.abort();
           } catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			result = e.getMessage().toString();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			result = e.getMessage().toString();
		}
		return result;
    }
    public static void main2(String[] args)
    {
    	     String json = "{\"name\":\"zhangsan\", \"age\":20, \"gender\": \"mail\"} ";
    	     String result = sendInfo("http://127.0.0.1:8080/prop/users", json);
    	     System.out.println(result);
    } 

}
