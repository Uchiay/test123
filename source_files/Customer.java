package com.company.billing;

public class Customer {
    private String customerId;
    private String type; // VIP or Regular
    private double creditLimit;

    public Customer(String customerId, String type, double creditLimit) {
        this.customerId = customerId;
        this.type = type;
        this.creditLimit = creditLimit;
    }

    public String getType() {
        return type;
    }

    public double getCreditLimit() {
        return creditLimit;
    }
}
