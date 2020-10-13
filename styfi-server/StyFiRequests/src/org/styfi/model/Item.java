package org.styfi.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.Entity;

@Entity
@Table(name="t_shirts")
public class Item implements Serializable{
	
	@Id
	@Column(name="t_shirt_id")
	private String t_shirt_id;
	
	@Column(name="url")
	private String url;
	
	@Column(name="item_name")
	private String item_name;
	
	@Column(name="shop")
	private String shop;
	
	@Column(name="gender")
	private String gender;
	
	@Column(name="price")
	private double price;
	
	@Column(name="created_at")
	private String created_at;

	public Item(){}

	public Item(String t_shirt_id, String url, String item_name, String shop,
			String gender, double price, String created_at) {
		super();
		this.t_shirt_id = t_shirt_id;
		this.url = url;
		this.item_name = item_name;
		this.shop = shop;
		this.gender = gender;
		this.price = price;
		this.created_at = created_at;
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
	
	
}
