package requests;


import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.Serializable;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;
import java.util.List;

import javax.imageio.ImageIO;

import org.styfi.model.Item;




public class testClass {
	
	
	static private final String USER_AGENT = "Mozilla/5.0";
	
	public static void main(String[] args) throws IOException, ClassNotFoundException {
		
		
		
		URL url = new URL("http://localhost:8080/StyFiServer/ImageUpload");
		HttpURLConnection con = (HttpURLConnection) url.openConnection();

		// optional default is GET
		con.setRequestMethod("GET");
		
		//con.getOutputStream()
		//add request header
		//con.setRequestProperty("User-Agent", USER_AGENT);
		
		BufferedImage img = ImageIO.read(new File("/home/ilja/git_repos/cv-sift-search/dataset_hm/2019_05_03_13_13_39_1.jpg.jpg"));
		ByteArrayOutputStream bos = new ByteArrayOutputStream();
	      ImageIO.write(img, "jpg", bos );
	      byte [] data = bos.toByteArray();
	      
	      con.setDoOutput(true);
	      OutputStream ops = con.getOutputStream();
	      ops.write(data);
	      ops.close();
		int responseCode = con.getResponseCode();
		System.out.println("\nSending 'GET' request to URL : " + url);
		System.out.println("Response Code : " + responseCode);

		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();

		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();

		//print result
		List<Item> items = (List<Item>) fromString(response.toString());
		System.out.println("Der beste Treffer hat die ID " + items.get(0).getT_shirt_id()
				+ " und heisst '" + items.get(0).getItem_name() 
				+ "'. Es ist erhaeltlich bei '" + items.get(0).getShop() 
				+ "' und kostet " + items.get(0).getPrice() 
				+ "Euro.");
		

	}
	
	private static Object fromString( String s ) throws IOException ,
       ClassNotFoundException {
		byte [] data = Base64.getDecoder().decode( s );
		ObjectInputStream ois = new ObjectInputStream( 
		new ByteArrayInputStream(  data ) );
		Object o  = ois.readObject();
		ois.close();
		return o;
	}

	/** Write the object to a Base64 string. */
	private static String toString( Serializable o ) throws IOException {
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		ObjectOutputStream oos = new ObjectOutputStream( baos );
		oos.writeObject( o );
		oos.close();
		return Base64.getEncoder().encodeToString(baos.toByteArray()); 
	}
}
