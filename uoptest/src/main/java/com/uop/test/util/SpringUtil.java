package com.uop.test.util;

import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.map.JsonMappingException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;


/**
 * spring工具类
 * @author 
 *
 */
public class SpringUtil {

	/**
	 * @param args
	 * @throws IOException 
	 * @throws JsonMappingException 
	 * @throws JsonGenerationException 
	 */
	public static void main(String[] args) throws JsonGenerationException, JsonMappingException, IOException {

		ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
	}

	private static ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

	public static Object getBean(String beanName) {
		String[] a = ctx.getBeanDefinitionNames();
//		for(String m:a)
//			System.out.println(m);
		return ctx.getBean(beanName);
	}

}
