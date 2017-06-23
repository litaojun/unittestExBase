package com.uop.test.util;

public class TestResultInfaces 
{
	private int facestatus = 0;
	private int faceTotalNum=0;
	private int facesucess=0;
	private int facefail=0;
	private int faceexcepiton=0;
	private String facename;
	public void setFacestatus(int faceStatus   )
	{
		this.facestatus = faceStatus;
	}
	public void setFaceTotalNum(int    faceTotalNum )
	{
		this.faceTotalNum = faceTotalNum;
	}
	public void setFacesucess(int    faceSucess   )
	{
		this.facesucess = faceSucess;
	}
	public void setFacefail(int    faceFail     )
	{
		this.facefail = faceFail;
	}
	public void setFaceexcepiton(int    faceExcepiton)
	{
		this.faceexcepiton = faceExcepiton;
	}
	public void setFacename(String facename     )
	{
		this.facename = facename;
	}
	
	public int getFacestatus()  
	{
		return this.facestatus;
	}
	public int getFaceTotalNum() 
	{
		return this.faceTotalNum;
		
	}
	public int getFacesucess()   
	{
		return this.facesucess;
	}
	public int getFacefail()    
	{
		return this.facefail;
	}
	public int getFaceexcepiton()
	{
	    return this.faceexcepiton;	
	}
	public String getFacename()
	{
		return this.facename;
		
	}

}
