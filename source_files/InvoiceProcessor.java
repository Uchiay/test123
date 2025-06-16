package com.company.billing;

public class InvoiceProcessor {
    private CustomerService customerService;
    private OrderService orderService;
    private DiscountService discountService;
    private ReviewService reviewService;

    public InvoiceProcessor(CustomerService customerService, OrderService orderService,
                            DiscountService discountService, ReviewService reviewService) {
        this.customerService = customerService;
        this.orderService = orderService;
        this.discountService = discountService;
        this.reviewService = reviewService;
    }

    public InvoiceResult processInvoice(String customerId, String orderId) {
        Customer customer = customerService.getCustomerById(customerId);
        OrderService order = orderService.getOrderById(orderId);

        double totalAmount = order.calculateTotal();
        double discount = discountService.calculateDiscount(customer, order);
        double finalAmount = totalAmount - discount;

        boolean requiresReview = reviewService.requiresManualReview(customer, order);

        InvoiceResult result = new InvoiceResult();
        result.setCustomerId(customerId);
        result.setOrderId(orderId);
        result.setTotalAmount(totalAmount);
        result.setDiscount(discount);
        result.setFinalAmount(finalAmount);
        result.setRequiresReview(requiresReview);

        return result;
    }
}
