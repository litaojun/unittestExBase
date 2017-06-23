package com.uop.test.util;

public class InterfaceConfig 
{
	//public static String ip="10.205.33.107";
	public static String timestr = "20170527090000";
	//public static String ip="10.205.68.20:10000";
	//https://uat-uop-api.opg.cn/item-service/showConfig/home
	public static String ip="uat-uop-api.opg.cn";
	public static String userImportURL = "https://"+ip+"/item-service/showConfig/home";
	public static String userAlertRL = "http://"+ip+"/ums/users";
	public static String guitGetUserURL = "http://"+ip+"/ums/users/guid/%s/prop";
	public static String phoneGetUserURL = "http://"+ip+"/ums/users/phoneNo/%s/prop";
	//public static String URL = "https://dev-api.opg.cn/prop/users/uuid/%s/nickhead";
	public static String uuidGetUserURL = "http://"+ip+"/ums/users/uuid/%s/prop";
	public static String guidGetTagsURL = "http://"+ip+"/ums/users/guid/%s/tags";
	public static String phoneGetTagsURL = "http://"+ip+"/ums/users/phoneNo/%s/tags";
	public static String uuidGetTagsURL = "http://"+ip+"/ums/users/uuid/%s/tags";
	public static String tagGetGuidsURL = "http://"+ip+"/ums/tags/tagCode/%s/users";
	public static String userCodesURL = "http://"+ip+"/passport/codes/%s";
	public static String registerUserURL = "http://"+ip+"/passport/mobile";
	public static String loginUserURL = "http://"+ip+"/passport/mobile/tokens";
	public static String OTPloginUserURL = "http://"+ip+"/passport/tokens/otp";
	public static String OTPActivatinUserURL = "http://"+ip+"/passport/mobile/activation";
	public static String userChangePasswdURL = "http://"+ip+"/passport/users/change-pwd";
	public static String userResetPasswdURL = "http://"+ip+"/passport/users/reset-pwd";
	public static String userTokenCheckURL = "http://"+ip+"/passport/users/validate-status";
}
