package com.uop.test.util;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;

public class AnnotationFilterClass 
{

	public static ArrayList<Class>  filterClassListByAnnotation(ArrayList<Class> classlist,Class a)
	{
		ArrayList<Class> retcls = new ArrayList<Class>();
		for(Class cs:classlist)
		{
			boolean sign = filterClassByAnnotation(cs,a);
			if(sign)
			{

				retcls.add(cs);
			}
		}
		return retcls;
	}
	public static boolean  filterClassByAnnotation(Class classs,Class aa)
	{  
		Method[] metd = classs.getMethods();
		boolean retsign = false;
		for(Method m:metd)
		{
			boolean hasAnnotation = m.isAnnotationPresent(aa);
			if(hasAnnotation)
			{
				retsign = true;
				break;
			}
		}
		return retsign;
	}
	
	public static ArrayList<Method>  filterMethodListByAnnotation(ArrayList<Class> classlist,Class a)
	{
		ArrayList<Method> retcls = new ArrayList<Method>();
		for(Class cs:classlist)
		{
			ArrayList<Method> clsmethod = getMethodFromClassByAnnotation(cs,a);
			retcls.addAll(clsmethod);
		}
		return retcls;
	}
	public static ArrayList<Method> getMethodFromClassByAnnotation(Class cls,Class a)
	{
		ArrayList<Method> retcls = new ArrayList<Method>();
		Method[] metd = cls.getMethods();
		for(Method md:metd)
		{
			boolean sign = md.isAnnotationPresent(a);
			if(sign)
				retcls.add(md);
		}
		return retcls;
	}
}
