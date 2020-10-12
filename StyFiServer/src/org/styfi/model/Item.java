package org.styfi.model;

import java.io.IOException;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.styfi.model.ItemFromDB;

public class Item implements Serializable{
	
	private static final long serialVersionUID = 1L;
	private byte[] image_as_byte_array;
	private String t_shirt_id;
	private String url;
	private String image_path;
	private String item_name;
	private String shop;
	private String gender;
	private double price;
	private String created_at;

	public Item(){}
	
	/* >>>>>>>> THIS CONSTRUCTOR IS CALLED FROM DATA PREPARATION CLASS <<<<<<< */
	public Item(String t_shirt_id, String url, byte[] image_as_byte_array, String item_name, String shop,
			String gender, double price, String created_at) {
		super();
		this.t_shirt_id = t_shirt_id;
		this.url = url;
		this.image_path = "NULL";
		this.item_name = item_name;
		this.shop = shop;
		this.gender = gender;
		this.price = price;
		this.created_at = created_at;
		
		this.image_as_byte_array = image_as_byte_array;
	}

	public String getT_shirt_id() {
		return t_shirt_id;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getImage_path() {
		return image_path;
	}

	public String getItem_name() {
		return item_name;
	}

	public void setItem_name(String item_name) {
		this.item_name = item_name;
	}

	public String getShop() {
		return shop;
	}

	public void setShop(String shop) {
		this.shop = shop;
	}

	public String getGender() {
		return gender;
	}

	public void setGender(String gender) {
		this.gender = gender;
	}

	public double getPrice() {
		return price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

	public String getCreated_at() {
		return created_at;
	}

	public void setCreated_at(String created_at) {
		this.created_at = created_at;
	}

	@Override
	public String toString() {
		return "Item [t_shirt_id=" + t_shirt_id + ", url=" + url
				+ ", item_name=" + item_name + ", shop=" + shop + ", gender="
				+ gender + ", price=" + price + ", created_at=" + created_at
				+ "]";
	}
	
	public byte[] getImage_as_byte_array(){
		return image_as_byte_array;
	}
	
}
