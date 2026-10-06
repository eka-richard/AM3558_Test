#include <linux/module.h>
#include <linux/init.h>

int can_init(void)
{
    printk("CAN Driver load done\n");

    return 0;
}

void can_exit(void)
{
    printk("CAN Driver unload done\n");
}

module_init(can_init);
module_exit(can_exit);

MODULE_LICENSE("GPL");
