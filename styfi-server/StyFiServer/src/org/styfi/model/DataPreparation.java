package org.styfi.model;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import org.styfi.model.Item;
import org.styfi.model.ItemFromDB;

public class DataPreparation {
	public static boolean DEBUG = false;
	
	public void setDebug(boolean debug) {
		DEBUG = debug;
	}
	
	static SessionFactory factory;
	
	public DataPreparation(){
		factory = new Configuration()
			.configure("hibernate.cfg.xml")
			.addAnnotatedClass(ItemFromDB.class)
			.buildSessionFactory();
	}
	
	public void finalize(){
		factory.close();
	}
	
	public Item get_item_by_id(String t_shirt_id, PrintWriter out) throws Exception{
		if(DEBUG) out.println("Getting item by ID:" + t_shirt_id + "\n");
		/* >>>>>>>> LOGIN TO THE DB <<<<<<< */
		Session session = factory.getCurrentSession();
		
		if(DEBUG) out.println("Starting transaction with DB...");
		
		session.beginTransaction();
		
		if(DEBUG) out.println("Querying item...");
		
		/* >>>>>>>> CONNECT TO THE DB AND EXECUTE THE QUERY <<<<<<< */
		ItemFromDB queryItemFromDB = session.get(ItemFromDB.class, t_shirt_id);
			
		session.getTransaction().commit();
			
		/* >>>>>>>> RETURN THE QUERY RESPONSE AS ITEM OBJECT INCLUDING THE IMAGE AS BYTE ARRAY <<<<<<< */
		//return new Item(queryItemFromDB);
		
		if(DEBUG) out.println("Generating Item java class...");
		
		return new Item(queryItemFromDB.getT_shirt_id(), queryItemFromDB.getUrl(), set_byte_array_from_imgpath(queryItemFromDB.getImage_path(), out), 
				queryItemFromDB.getItem_name(), queryItemFromDB.getShop(),
				queryItemFromDB.getGender(), queryItemFromDB.getPrice(), queryItemFromDB.getCreated_at());
	}
	
	private byte[] set_byte_array_from_imgpath(String image_path, PrintWriter out){
		if(DEBUG) out.println("Setting byte array...");
		Path path = Paths.get(image_path);
		
		byte[] data;
		try {
			data = Files.readAllBytes(path);
			return data;
		} catch (IOException e) {
			out.println(e);
			e.printStackTrace();
		}
		
		return null;
	}
	
	public static void main(String[] args) {
		
		DataPreparation dP = new DataPreparation();
		
		/*
		try{
			Item myItem = dP.get_item_by_id("2019_05_03_11_07_36");

			System.out.println("Shop: " + myItem.getItem_name());
			
			System.out.println("Item Name: " + myItem.getItem_name());
			
			System.out.println("Price: " + myItem.getPrice());
			
		}catch (Exception e) {
			e.printStackTrace();
		}
		*/
		
		
		dP.finalize();
	}

}
