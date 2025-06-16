package com.company.billing;

public class ReviewService {
    public boolean requiresManualReview(Customer customer, OrderService order) {
        return order.calculateTotal() > customer.getCreditLimit();
    }
}
