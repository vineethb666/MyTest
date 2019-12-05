
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class Insert {

	/**
	 * @param args
	 */
	public  void findFiles(String dirLoc,String restUrl)
	{
         
	       File []files=    new File(dirLoc).listFiles();
	       for (int i = 0; i < files.length; i++)
	       {
               if(files[i].getName().equals("com.codex"))
               {
            	   continue;
               }

			      if (files[i].isDirectory())
			      {

			    	  findFiles(files[i].getAbsolutePath(),restUrl);

				  }
			      else{

						 if(files[i].getName().endsWith(".rb"))
					      {
					    	  
					    	String  fileName=files[i].getName();
					    	System.out.println(fileName+"***");

					    	 try {
					    		 printFile(files[i].getAbsolutePath(), restUrl,fileName);
					    		 
					    	  } catch (Exception e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}


					      }
					 }


	       }


	}

	public  List<String> insertRest(String filepath, String restUrl, String fileName)
	{
		List<String> store= new ArrayList<String>();
		List<String> rList=null;
		FileReader fr;
		try {
			fr = new FileReader(filepath);
			BufferedReader br= new BufferedReader(fr);
			String stemp= br.readLine();
			store.add(stemp);
			while(stemp!=null)
			{
				stemp=br.readLine();
				store.add(stemp);
			}
			RestInsert restInserted= new RestInsert();
		    rList=restInserted.findAndInsert(store, restUrl,fileName);
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return rList;
	}
	public void printFile(String filepath, String restUrl,String fileName)
	{
		 List<String> rList= insertRest( filepath,  restUrl,fileName);
		 File file= new File(filepath);
		 try {
			FileWriter fw = new FileWriter(file);
			PrintWriter pw= new PrintWriter(fw);
			for(int i=0;i<rList.size();i++)
			{
				pw.println(rList.get(i));
			}
			pw.flush();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
}
