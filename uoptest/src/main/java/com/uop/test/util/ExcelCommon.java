package com.uop.test.util;

import java.io.FileInputStream;
import java.io.IOException;

import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class ExcelCommon 
{
	private XSSFSheet  mySheet=null;
	private XSSFWorkbook  wb=null;
	public ExcelCommon(String filePath,String sheetName) throws IOException
	{
		wb = new XSSFWorkbook (new FileInputStream(filePath));
		mySheet = wb.getSheet(sheetName);
	}
	public void closeExcel() throws IOException
	{
		this.wb.close();
	}
	public String readStrByRowOrCell(int row,int cell)
	{
		//System.out.println("row="+row+";cell="+cell+mySheet);
		XSSFRow datarow = mySheet.getRow(row+1);
		//System.out.println("datarow="+datarow+"datarow.getFirstCellNum()="+datarow.getFirstCellNum());
		XSSFCell  dataCell = datarow.getCell((short)(cell));
		//System.out.println("dataCell="+dataCell);
		//System.out.println("dataCell.getCellType()"+dataCell.getCellType());
		if(dataCell == null)
			return null;
		Object val;
		switch (dataCell.getCellType()) {
		case XSSFCell.CELL_TYPE_STRING:
		val = dataCell.getStringCellValue();
		break;
		case XSSFCell.CELL_TYPE_NUMERIC:
		if ("@".equals(dataCell.getCellStyle().getDataFormatString())) {
		val =dataCell.getNumericCellValue();
		} else if ("General".equals(dataCell.getCellStyle().getDataFormatString())) {
		val = dataCell.getNumericCellValue();
		} else {
		val =dataCell.getNumericCellValue();
		}
		break;
		case XSSFCell.CELL_TYPE_BOOLEAN:
		val = dataCell.getBooleanCellValue();
		break;
		case XSSFCell.CELL_TYPE_BLANK:
		val = "";
		break;
		default:
		val = dataCell.toString();
		break;
		}
		//System.out.println("val.toString()"+val.toString());
		return val.toString();
		
	}
	public String[][] readSheetToArray(int row,int cell)
	{
		String[][] a=new String[row][cell];
		for(int i=0;i<row;i++)
		{
			for(int j=0;j<cell;j++)
			{
				//System.out.println("i="+i+";j="+j+"a[i][j]="+this.readStrByRowOrCell(i, j));
				a[i][j]=this.readStrByRowOrCell(i, j);
			}
		}
		return a;
	}
	public void writeSheet(String data,int row,int cell)
	{
		XSSFCell  dataCell = mySheet.getRow(row).getCell(cell);
		dataCell.setCellValue(data);
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
