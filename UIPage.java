import javax.swing.*;  
import java.awt.*;  
import java.awt.event.*; 
public class UIPage  {
	JFrame frame;
	  JLabel heading; JButton browse;    private JProgressBar progressBar;
	   private Task task;JDialog dlg; private boolean flag= false; JDialog message;
	 UIPage(){  
		  frame = new JFrame("vin_code");	 	  
		  heading= new JLabel("FAST DEBUG");
		  Font font = new Font("Courier New", Font.BOLD, 25);
		  heading.setFont(font);
		  heading.setBounds(250, 10, 200, 50);
		  heading.setHorizontalAlignment(JLabel.CENTER);
		  heading.setVerticalAlignment(JLabel.CENTER);
		  
		    dlg = new JDialog(frame, "Progress Dialog", true);
		    progressBar = new JProgressBar(0, 500);
		    dlg.add(BorderLayout.CENTER, progressBar);
		    dlg.add(BorderLayout.NORTH, new JLabel("Progress..."));
		    dlg.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
		    dlg.setSize(300, 75);
		    dlg.setLocationRelativeTo(frame);
		 	
		    message= new JDialog(frame, "alert message", true);
		    message.add(BorderLayout.CENTER, new JLabel("Please browse the directory!!"));
		    message.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
		    message.setSize(300, 70);
		    message.setLocationRelativeTo(frame);
		    
		    
		  JTextField bpath= new JTextField();
		  bpath.setToolTipText("browse source code root folder !!");
		  bpath.setBounds(50, 80, 350, 25);
		  JButton browse= new JButton("Browse");
		  browse.setToolTipText("browse source code root folder!!");
		  browse.setBounds(450, 80, 100, 25);
		  browse.addActionListener(new ActionListener()
		  {
			  public void actionPerformed(ActionEvent e)
			  {
			    // display/center the jdialog when the button is pressed
				  JFileChooser jchose = new JFileChooser();
		        	jchose.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		        	Integer opt = jchose.showSaveDialog(frame);
		        	if(opt == JFileChooser.APPROVE_OPTION) {
		        	    bpath.setText(jchose.getSelectedFile().getPath());
		        	}
			    
			  }
			});
		  
		  JButton start= new JButton("Start");
		  start.setBounds(450, 380, 100, 25);
		
		  start.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
			  String dirLoc= bpath.getText();
					if(!dirLoc.equals(""))
					{
						 task = new Task();                
				         task.start();
						 
						Insert insert= new Insert();
						insert.findFiles(dirLoc, "http://restUrl");
						flag=true;
					}
							
				else
				{
				Message mes= new Message();
				mes.start();
				}
			}
		});
		  
		  
		
		  frame.add(heading);
		  frame.add(bpath);
		  frame.add(browse);
		  frame.add(start);
		  frame.setSize(700,500);  
		  frame.setLayout(new BorderLayout());  
		  frame.setVisible(true);
		  frame.setResizable(false);
		  frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		  
	    }  
	 
	   
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new UIPage();
	
	}
	
 private class Task extends Thread {    
	      public Task(){
	      }
	      public void run(){
	    	  Visible vis = new Visible();
	    	  vis.start();
	    	 for (int i = 0; i <= 500; i++) {
	    	     
	    	      progressBar.setValue(i);
	    	      if(progressBar.getValue()==500&&flag==true){
	    	        dlg.setVisible(false);
	    	        System.exit(0);
	    	        
	    	      }
	    	      try {
	    	        Thread.sleep(25);
	    	      } catch (InterruptedException e) {
	    	        e.printStackTrace();
	    	      }
	    	    }
	      }
	      
	  }
 class Visible extends Thread
 {
	
	 public void run()
	 {
		 dlg.setVisible(true);
	 }
	 
 }
 class Message extends Thread
 {

	 public void run()
	 {
		 message.setVisible(true);
	 }
	 
 }
 
}


 
 