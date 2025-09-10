<script lang="ts">
    import { onMount } from 'svelte';
    import type { Product } from '$lib/types';

    let products: Product[] = [];
    let loading = true;
    let error: string | null = null;
    let searchQuery = '';
    let sortBy = 'price-low';
    let showAddModal = false;

    // New product form
    let newProduct = {
        name: '',
        price: 0,
        stock: 0
    };

    async function refreshProducts() {
        try {
            const res = await fetch('/products');
            if (!res.ok) throw new Error('Failed to fetch products');
            products = await res.json();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            loading = false;
        }
    }

    async function addProduct() {
        try {
            const res = await fetch('/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newProduct),
            });

            if (!res.ok) throw new Error('Failed to add product');
            
            await refreshProducts();
            showAddModal = false;
            newProduct = { name: '', price: 0, stock: 0 };
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }

    async function deleteProduct(id: number) {
        if (!confirm('Are you sure you want to delete this product?')) return;
        
        try {
            const res = await fetch(`/products/${id}`, {
                method: 'DELETE',
            });

            if (!res.ok) throw new Error('Failed to delete product');
            await refreshProducts();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }

    onMount(refreshProducts);

    $: filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(searchQuery.toLowerCase())
    ).sort((a, b) => {
        if (sortBy === 'price-low') return a.price - b.price;
        if (sortBy === 'price-high') return b.price - a.price;
        return a.name.localeCompare(b.name);
    });
</script>

<div class="container">
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/products">Products</a></li>
        </ul>
    </nav>

    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>All Products</h1>
        <div>
            <button on:click={() => showAddModal = true}>Add Product</button>
        </div>
    </div>

    <div style="margin-bottom: 20px;">
        <div style="display: flex; gap: 20px;">
            <div>
                <label for="search">Search: </label>
                <input id="search" type="text" placeholder="Search products..." bind:value={searchQuery} />
            </div>
            <div>
                <label for="sort">Sort by: </label>
                <select id="sort" bind:value={sortBy}>
                    <option value="price-low">Price: Low to High</option>
                    <option value="price-high">Price: High to Low</option>
                    <option value="name">Name</option>
                </select>
            </div>
        </div>
    </div>

    {#if loading}
        <div style="text-align: center; padding: 20px;">
            Loading...
        </div>
    {:else if error}
        <div style="color: red; border: 1px solid red; padding: 10px; margin: 10px 0;">
            {error}
        </div>
    {:else}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Price</th>
                    <th>Stock</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {#each filteredProducts as product}
                    <tr>
                        <td>{product.id}</td>
                        <td>
                            <a href="/products/{product.id}">{product.name}</a>
                        </td>
                        <td>${product.price.toFixed(2)}</td>
                        <td>{product.stock} units</td>
                        <td>
                            <a href="/products/{product.id}" style="margin-right: 1rem;">View</a>
                            <button 
                                class="btn-danger"
                                on:click={() => deleteProduct(product.id)}
                            >
                                Delete
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {/if}

    {#if showAddModal}
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center;">
        <div style="background: white; padding: 20px; border-radius: 5px; width: 300px;">
            <h3 style="margin-top: 0;">Add New Product</h3>
            <form on:submit|preventDefault={addProduct}>
                <div style="margin-bottom: 10px;">
                    <label for="name">Product Name</label>
                    <input id="name" required bind:value={newProduct.name} style="width: 100%; padding: 5px;" />
                </div>
                <div style="margin-bottom: 10px;">
                    <label for="price">Price</label>
                    <input id="price" type="number" step="0.01" required bind:value={newProduct.price} style="width: 100%; padding: 5px;" />
                </div>
                <div style="margin-bottom: 10px;">
                    <label for="stock">Stock</label>
                    <input id="stock" type="number" required bind:value={newProduct.stock} style="width: 100%; padding: 5px;" />
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 10px;">
                    <button type="button" on:click={() => showAddModal = false}>Cancel</button>
                    <button type="submit" style="background-color: blue; color: white;">Add Product</button>
                </div>
            </form>
        </div>
    </div>
    {/if}
</div>
