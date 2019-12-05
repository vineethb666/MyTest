import java.util.ArrayList;
import java.util.List;

public final class RestInsert {
 
	 public List<String> findAndInsert(List<String> list, String restUrl, String fileName)
	 {
		 List<String> mList = list;
		 List<Integer> iList= new ArrayList<Integer>();
		 List<String> nList = new ArrayList<String>();
		 StringBuilder sb= new StringBuilder("");
		 for(int i=0;i<mList.size();i++)
		 {
		String temp= mList.get(i);
		if(temp==null)
		{
			temp= " ";
		}
		String arr[]= temp.split(" ");
		for(int j=0;j<arr.length;j++)
		  {
			if(arr[j].equals("def"))
			 {
				iList.add(i+1);	
				while(j+1<arr.length)
				{
					sb.append(arr[j+1]+" ");
					j++;
				}
				nList.add(sb.toString());
			 }
			
		   }
			 sb= new StringBuilder("");
		 }
		 for(int i=0;i<iList.size();i++)
		 {
			 mList.set(iList.get(i), restUrl+"/"+fileName+"/"+nList.get(i));
			 
		 }
		
		 
		 return mList;
	 }
	
}
