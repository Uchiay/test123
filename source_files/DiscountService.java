package com.company.billing;

public class DiscountService {
    public double calculateDiscount(Customer customer, OrderService order) {
        if ("VIP".equals(customer.getType()) && order.calculateTotal() > 1000) {
            return order.calculateTotal() * 0.10;
        }
        return 0.0;
    }
}
