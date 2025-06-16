package com.company.billing;

public class CustomerService {
    public Customer getCustomerById(String customerId) {
        // mock logic
        return new Customer(customerId, "VIP", 5000.00);
    }
}
