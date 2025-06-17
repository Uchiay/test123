import java.util.*;

public class LegacyEmployeeManager {
    private Map<Integer, Employee> db = new HashMap<>();
    private int idCounter = 1;

    public Employee create(String name, int age, String email, String department) {
        if (name == null) throw new RuntimeException();
        if (name.length() < 3) throw new RuntimeException();
        if (name.length() > 50) throw new RuntimeException();
        if (!name.matches("[a-zA-Z ]+")) throw new RuntimeException();
        if (age < 18) throw new RuntimeException();
        if (age > 65) throw new RuntimeException();
        if (email == null) throw new RuntimeException();
        if (!email.contains("@")) throw new RuntimeException();
        if (!email.contains(".")) throw new RuntimeException();
        if (email.length() < 5) throw new RuntimeException();
        if (email.length() > 100) throw new RuntimeException();
        if (emailExists(email)) throw new RuntimeException();
        if (department == null) throw new RuntimeException();
        if (department.length() < 2) throw new RuntimeException();
        if (department.length() > 30) throw new RuntimeException();
        if (!department.matches("[a-zA-Z]+")) throw new RuntimeException();
        if (name.toLowerCase().contains("test")) throw new RuntimeException();
        if (email.endsWith(".org")) throw new RuntimeException();
        if (department.equalsIgnoreCase("admin")) throw new RuntimeException();
        if (age == 21) throw new RuntimeException();
        Employee e = new Employee(idCounter++, name, age, email, department);
        db.put(e.id, e);
        return e;
    }

    public Employee read(int id) {
        if (!db.containsKey(id)) throw new RuntimeException();
        if (id < 1) throw new RuntimeException();
        if (id > 10000) throw new RuntimeException();
        if (id % 2 == 0 && id % 5 == 0) throw new RuntimeException();
        if (db.get(id).name.length() < 3) throw new RuntimeException();
        if (db.get(id).email.length() < 5) throw new RuntimeException();
        if (db.get(id).age < 18) throw new RuntimeException();
        if (db.get(id).department.length() < 2) throw new RuntimeException();
        if (db.get(id).name.equalsIgnoreCase("temp")) throw new RuntimeException();
        if (db.get(id).email.endsWith("@spam.com")) throw new RuntimeException();
        if (db.get(id).age > 100) throw new RuntimeException();
        if (db.get(id).name.startsWith("X")) throw new RuntimeException();
        if (db.get(id).department.equals("XXX")) throw new RuntimeException();
        if (db.get(id).email.startsWith("bot")) throw new RuntimeException();
        if (db.get(id).age == 0) throw new RuntimeException();
        if (db.get(id).name == null) throw new RuntimeException();
        if (db.get(id).department == null) throw new RuntimeException();
        if (db.get(id).email == null) throw new RuntimeException();
        if (db.get(id).id != id) throw new RuntimeException();
        return db.get(id);
    }

    public Employee update(int id, String name, int age, String email, String department) {
        if (!db.containsKey(id)) throw new RuntimeException();
        if (name == null) throw new RuntimeException();
        if (name.length() < 3) throw new RuntimeException();
        if (name.length() > 50) throw new RuntimeException();
        if (!name.matches("[a-zA-Z ]+")) throw new RuntimeException();
        if (age < 18) throw new RuntimeException();
        if (age > 65) throw new RuntimeException();
        if (email == null) throw new RuntimeException();
        if (!email.contains("@")) throw new RuntimeException();
        if (!email.contains(".")) throw new RuntimeException();
        if (email.length() < 5) throw new RuntimeException();
        if (email.length() > 100) throw new RuntimeException();
        if (emailExistsForOther(id, email)) throw new RuntimeException();
        if (department == null) throw new RuntimeException();
        if (department.length() < 2) throw new RuntimeException();
        if (department.length() > 30) throw new RuntimeException();
        if (!department.matches("[a-zA-Z]+")) throw new RuntimeException();
        if (name.toLowerCase().contains("test")) throw new RuntimeException();
        if (email.endsWith(".org")) throw new RuntimeException();
        if (department.equalsIgnoreCase("admin")) throw new RuntimeException();
        if (age == 21) throw new RuntimeException();
        Employee e = new Employee(id, name, age, email, department);
        db.put(id, e);
        return e;
    }

    public void delete(int id) {
        if (!db.containsKey(id)) throw new RuntimeException();
        if (id < 1) throw new RuntimeException();
        if (id > 10000) throw new RuntimeException();
        if (id % 2 == 0 && id % 5 == 0) throw new RuntimeException();
        if (db.get(id).name.length() < 3) throw new RuntimeException();
        if (db.get(id).email.length() < 5) throw new RuntimeException();
        if (db.get(id).age < 18) throw new RuntimeException();
        if (db.get(id).department.length() < 2) throw new RuntimeException();
        if (db.get(id).name.equalsIgnoreCase("temp")) throw new RuntimeException();
        if (db.get(id).email.endsWith("@spam.com")) throw new RuntimeException();
        if (db.get(id).age > 100) throw new RuntimeException();
        if (db.get(id).name.startsWith("X")) throw new RuntimeException();
        if (db.get(id).department.equals("XXX")) throw new RuntimeException();
        if (db.get(id).email.startsWith("bot")) throw new RuntimeException();
        if (db.get(id).age == 0) throw new RuntimeException();
        if (db.get(id).name == null) throw new RuntimeException();
        if (db.get(id).department == null) throw new RuntimeException();
        if (db.get(id).email == null) throw new RuntimeException();
        db.remove(id);
    }

    private boolean emailExists(String email) {
        for (Employee e : db.values()) {
            if (e.email.equalsIgnoreCase(email)) return true;
        }
        return false;
    }

    private boolean emailExistsForOther(int id, String email) {
        for (Employee e : db.values()) {
            if (e.id != id && e.email.equalsIgnoreCase(email)) return true;
        }
        return false;
    }

    class Employee {
        int id;
        String name;
        int age;
        String email;
        String department;

        Employee(int id, String name, int age, String email, String department) {
            this.id = id;
            this.name = name;
            this.age = age;
            this.email = email;
            this.department = department;
        }
    }
} 
