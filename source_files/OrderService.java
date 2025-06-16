package com.company.billing;

public class OrderService {
    private String orderId;
    private double itemTotal;
    private double tax;

    public OrderService(String orderId, double itemTotal, double tax) {
        this.orderId = orderId;
        this.itemTotal = itemTotal;
        this.tax = tax;
    }

    public double calculateTotal() {
        return itemTotal + tax;
    }

    public String getOrderId() {
        return orderId;
    }
}
